import threading
import socket
import json
import logging
from server import Server
from SM import StateMachine
from concurrent.futures import ThreadPoolExecutor


class ConcurrentStateMachineServer(Server):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.sm = StateMachine()

    def handle_client(self, client_socket):
        """
        Gestiona la conexión con un cliente. Recibe los datos del cliente, los procesa y envía una respuesta.

        Args:
            client_socket (tuple): (host, port)
        """
        try:
            # Recibir datos del cliente
            data = client_socket.recv(1024).decode().strip()
            print(f'Data received from client: {data}')

            # Deserializar datos
            data = json.loads(data)

            # Procesar los datos
            response = self.sm._transition(data)

            # Enviar respuesta al cliente
            client_socket.sendall(str(response).encode())

        except Exception as e:
            print(f"Error handling client: {e}")

        finally:
            # Cerrar el socket del cliente
            client_socket.close()

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
                client_socket, client_address = server_socket.accept()
                print(f'Client connected from {client_address}')
                logging.info(f'Client connected from {client_address}')
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
                client_thread.start()
                server_socket.close()
