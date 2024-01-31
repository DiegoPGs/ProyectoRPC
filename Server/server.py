import socket

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345

# Define the initial state
state = 'INITIAL'

# Define the state machine transitions
transitions = {
    'INITIAL': {
        'HELLO': 'GREETING',
        'EXIT': 'EXIT'
    },
    'GREETING': {
        'HOWAREYOU': 'FEELING',
        'EXIT': 'EXIT'
    },
    'FEELING': {
        'GOOD': 'THANKS',
        'BAD': 'SORRY',
        'EXIT': 'EXIT'
    },
    'SORRY': {
        'EXIT': 'EXIT'
    },
    'THANKS': {
        'EXIT': 'EXIT'
    },
    'EXIT': {}
}

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((SERVER_ADDRESS, SERVER_PORT))

# Listen for incoming connections
server_socket.listen(1)
print(f'Server listening on {SERVER_ADDRESS}:{SERVER_PORT}')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print(f'Client connected from {client_address}')

    # Receive data from the client
    data = client_socket.recv(1024).decode().strip()

    # Process the client request and transition the state
    if state == 'EXIT':
        response = 'Goodbye!'
    elif data in transitions[state]:
        state = transitions[state][data]
        response = f'Current state: {state}'
    else:
        response = 'Invalid request'

    # Send the response back to the client
    client_socket.send(response.encode())

    # Close the client connection
    client_socket.close()