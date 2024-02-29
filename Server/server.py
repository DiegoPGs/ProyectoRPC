class Server:
    """
    ### Server class.
    """
    def __init__(self, host, port):
        """
        ### Initialize the server.

        Args:
            host (str): The server host.
            port (int): The server port.
        """
        self.host = host
        self.port = port


# Define the server address and port
SERVER_ADDRESS = 'localhost'
#SERVER_ADDRESS = '0.0.0.0'
SERVER_PORT = 8080
