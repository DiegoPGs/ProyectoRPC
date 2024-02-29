import threading
import socket
import json
import logging
import queue
from server import Server
from SM import StateMachine
from concurrent.futures import ThreadPoolExecutor
from configs import SERVER_ADDRESS, SERVER_PORTS


class ConcurrentStateMachineServer(Server):
    """
    Clase para el servidor concurrente que maneja una máquina de estados.

    Utiliza dos hilos: 
    uno para escuchar solicitudes y replicarlas a otros servidores
    otro para realizar la transición de la operación en la petición para la máquina de estados.
    """
    # zonas críticas para el servidor
    buffer = queue.Queue(maxsize=7) # buffer intermedio
    # fin de zonas críticas

    def __init__(self, host, port):
        super().__init__(host, port)
        self.sm = StateMachine()
        self.lock = threading.Lock() # lock para zonas críticas

    def replicar_peticion(self, data):
        """
        Replicar la petición a todos los servidores.

        data (dict): Datos de la petición codificados.
        """
        for port in SERVER_PORTS:
            if port != self.port:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((SERVER_ADDRESS, port))
                        s.sendall(json.dumps(data))
                        response = s.recv(1024).decode()
                        print(f'Replica from {port}: {response}')
                        logging.info(f'Replica from {port}: {response}')
                except Exception as e:
                    print(f"Error replicating request: {e}")

    def handle_client(self, client_socket):
        """
        Gestiona la conexión con un cliente. Recibe los datos del cliente, los procesa y envía una respuesta.

        Args:
            client_socket (tuple): (host, port)
        """
        with self.lock:
            try:
                # Recibir datos del cliente
                data = client_socket.recv(1024).decode().strip()
                print(f'Data received from client: {data}')
                logging.info(f'Data received from client: {data}')

                # Insertar datos en el buffer
                self.buffer.put(data, block=True, timeout=1)
                logging.info(f'Data into queue: {data}')

                # Replicar petición a otros servidores
                self.replicar_peticion(data)

            except Exception as e:
                print(f"Error handling client: {e}")

            finally:
                # Cerrar el socket del cliente
                client_socket.close()

    def consumir_peticion(self):
        """
        Consume la petición de la cola de peticiones.
        Mandar a llamar la trnasición de la máquina de estados y escribe un log.
        """
        with self.lock:
            try:
                # Deserializar datos
                data = json.loads(self.buffer.get(block=True, timeout=1))
                print(f'Consuming request: {data}')
                # Log request
                logging.info(f'Consuming request: {data}')

                # Procesar los datos
                response = self.sm.transition(data)
                print(f'Response: {response}')
                # Log response
                logging.info(f'Response: {response}')

            except queue.Empty:
                print("Buffer vacío, esperando")
            except Exception as e:
                print(f"Error consuming request: {e}")

    def start(self):
        """
        Inicia el servidor y escucha las conexiones entrantes.
        Utiliza threads para manejar múltiples conexiones de clientes.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)  # Esperar por conexiones entrantes, hasta 5 en cola
        print(f'Server listening on {self.host}:{self.port}')

        with ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                # Aceptar conexiones entrantes
                client_socket, client_address = server_socket.accept()
                print(f'Client connected from {client_address}')
                logging.info(f'Client connected from {client_address}')
                # Crear un nuevo hilo para manejar la interconexión
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                producer_thread = threading.Thread(target=self.consumir_peticion)
                # Iniciar el hilo
                client_thread.start()
                producer_thread.start()

                server_socket.close()

if __name__ == '__main__':
    threads = []
    for port in SERVER_PORTS:
        server = ConcurrentStateMachineServer(SERVER_ADDRESS, port)
        thread = threading.Thread(target=server.start)
        thread.start()
        threads.append(thread)
