import socket
import logging
import json

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8080

# Set up logger
logging.basicConfig(filename='logs.log', level=logging.INFO)

class Client:
    """
    ### Client class.
    """
    def __init__(self, host, port):
        """
        ### Initialize the client.

        Args:
            host (str): The server host.
            port (int): The server port.
        """
        self.host = host
        self.port = port

    def send_request(self, request):
        """
        ### Send a request to the server and print the response.

        Args:
            request (_type_): The request to send to the server.
        """
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        server_address = (self.host, self.port)

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

def main():
    # Create the client
    client = Client(SERVER_ADDRESS, SERVER_PORT)

    # Define the data to send to the server
    data = {'key': 0, 'value': 10.1, 'operation': 'set'}
    
    # Serialize the data
    data = json.dumps(data)

    # Send a request to the server
    response = client.send_request(data)

    print(f"Response: {response}")

if __name__ == '__main__':
    main()