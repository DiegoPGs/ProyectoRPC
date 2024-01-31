import socket
from StateMachine.SM import StateMachine
from server import Server
from server import SERVER_ADDRESS, SERVER_PORT


class StateMachineServer(Server):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.sm = StateMachine()

        def start(self):
            """
            ### Start the server.
            """
            # Create a socket object
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind the socket to the server address and port
            server_socket.bind((self.host, self.port))

            # Listen for incoming connections
            server_socket.listen(1)
            print(f'Server listening on {self.host}:{self.port}')

            # Accept a client connection
            while True:
                client_socket, client_address = server_socket.accept()
                print(f'Client connected from {client_address}')

                # Receive data from the client
                data = client_socket.recv(1024).decode().strip()
                print(f'Data received from client: {data}')

                # Process the client request and transition the state
                #response = self.sm.transition(data)
                
                # Send the response back to the client
                #client_socket.send(response.encode())

                # Close the client connection
                client_socket.close()

def main():
    """
    ### Main function.
    """
    # Create the server
    server = StateMachineServer(SERVER_ADDRESS, SERVER_PORT)

    # Start the server
    server.start()

if __name__ == '__main__':
    main()
