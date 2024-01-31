import socket

def send_request(request):
    """
    ### Send a request to the server and print the response.

    Args:
        request (_type_): The request to send to the server.
    """
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('localhost', 12345)

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Send the request to the server
        client_socket.sendall(request.encode())

        # Receive the response from the server
        response = client_socket.recv(1024).decode()

        # Print the response
        print(f"Response from server: {response}")

    finally:
        # Close the socket
        client_socket.close()

# Example usage
send_request("GET /state HTTP/1.1\r\nHost: localhost\r\n\r\n")