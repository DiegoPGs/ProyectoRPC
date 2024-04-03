import sys
import threading
import socket
import json
import logging
import queue
from server import Server
from SM import StateMachine
from concurrent.futures import ThreadPoolExecutor
from configs import SERVER_ADDRESS, SERVER_PORTS

"""
Tabla de registros:
{
    [host, port]: {
        data
    }
}

Datagrama

{
    "operation":{
        "action":
        "key":
        "value":
    }
}

"""
logging.basicConfig(filename='logs.log', level=logging.INFO)
class Peer(Server):
    """
    Clase para el servidor concurrente que maneja una máquina de estados.

    Utiliza dos hilos: 
    uno para escuchar solicitudes y replicarlas a otros servidores
    otro para realizar la transición de la operación en la petición para la máquina de estados.
    """
    # contador de lamport
    count : int = 0
    # zonas críticas para el servidor
    buffer = queue.Queue(maxsize=7) # buffer intermedio
    # fin de zonas críticas

    def __init__(self, host, port):
        super().__init__(host, port)
        self.sm = StateMachine()
        self.lock = threading.Lock() # lock para zonas críticas
        self.registros = {} # registros de peticiones || TODO: reemplazar con BD potencialmente

    def replicar_peticion(self, data):
        """
        Replicar la petición a todos los servidores.

        data (dict): Datos de la petición codificados.
        """
        # Replicar petición a otros servidores
        for port in set(SERVER_PORTS) - {self.port}: # Todos los servidores excepto el actual
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((SERVER_ADDRESS, port))
                        s.sendall(data.encode())
                        response = s.recv(1024).decode()
                        print(f'Replica from {port}: {response}')
                        logging.info(f'Replica from {port}: {response}')
                except Exception as e:
                    print(f"Error replicating request: {e}")
                    logging.error(f"Error replicating request: {e}")

    def handle_client(self, client_socket : socket.socket):
        """
        Gestiona la conexión con un cliente. Recibe los datos del cliente, los procesa y envía una respuesta.

        Args:
            client_socket (tuple): (host, port)
        """
        # Validar si la petición ha llegado con anterioridad
        #if (client_socket., client_address) in self.registros:
        #    return
        try:
            # Recibir datos del cliente
            data = client_socket.recv(1024).decode().strip()
            print(f'Data received from client: {data}')
            logging.info(f'Data received from client: {data}')

            # Encode data
            data = json.loads(data.encode())
            print(f'Data: {data}')

            ttl = data.get('ttl')
            print(f'TTL: {ttl}')

            if ttl > 0:
                data['ttl'] = ttl - 1

                # Insertar datos en el buffer
                self.buffer.put(data, block=True, timeout=1)
                logging.info(f'Data into queue: {data}')

                # Deserializar datos
                data = json.dumps(data)

                # Replicar petición a otros servidores
                self.replicar_peticion(data)
                print('Replicating request')
                logging.info('Replicating request')

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
        try:
            # Deserializar datos
            data = json.dumps(self.buffer.get(block=True, timeout=1))
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
            logging.info("Buffer vacío, esperando")
        except Exception as e:
            print(f"Error consuming request: {e}")
            logging.error(f"Error consuming request: {e}")

    def start(self):
        """
        Inicia el servidor y escucha las conexiones entrantes.
        Utiliza threads para manejar múltiples conexiones de clientes.
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(7)  # Esperar por conexiones entrantes, hasta 7 en cola
        print(f'Server listening on {self.host}:{self.port}')
        logging.info(f'Server listening on {self.host}:{self.port}')

        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                while True:
                    # Aceptar conexiones entrantes
                    client_socket, client_address = server_socket.accept()
                    print(f'Client connected from {client_address}')
                    logging.info(f'Client connected from {client_address}')
                    # Crear un nuevo hilo para manejar la interconexión
                    client_thread = threading.Thread(target=self.handle_client, args=(client_socket,)) # reads
                    producer_thread = threading.Thread(target=self.consumir_peticion)                  # writes
                    # Iniciar el hilo
                    client_thread.start()
                    producer_thread.start()
        finally:
            server_socket.close()

    def send_request(self, request, host, port):
        """
        ### Send a request to the server and print the response.

        Args:
            request (_type_): The request to send to the server.
        """
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        server_address = (host, port)

        response = None
        try:
            # Connect to the server
            client_socket.connect(server_address)

            # Send the request to the server
            client_socket.sendall(request.encode())

            # Receive the response from the server
            response = client_socket.recv(1024).decode()

            # Print the response
            print(f"Response from server: {response}")

        except Exception as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")

        finally:
            # Close the socket
            client_socket.close()

        # Return the response
        return response

if __name__ == '__main__':
    # usar argumentos de línea de comandos para el puerto
    puerto = int(sys.argv[1])

    # Crear un nuevo servidor
    peer = Peer(SERVER_ADDRESS, puerto)
    peer.start()