"""
#### Instrucciones de proyecto
En el primer proyecto se solicita programar una aplicación usando RPC (RMI). Se debe contar con varios clientes que envían solicitudes a un servidor.

El servidor debe tener una máquina de estado (SM) muy sencilla que ejecute las solicitudes de los clientes.

(Schneider, 1990) “A state machine consists of state variables, which encode its state, and commands, which transform its state. Each command is implemented by a deterministic program; execution of the command modifies the state variables and/or produces some output. The defining characteristic of a state machine is that it specifies a deterministic computation that reads a stream of requests and processes each, occasionally producing output.”

De las operaciones CRUD nos quedaremos solo con Read y Update (solo podremos, después, leer y modificar un campo de un registro de una tabla de la base de datos).

Modelamos el estado de la SM con un objeto. El objeto tiene un diccionario que almacena valores reales y métodos (comandos) públicos get(key), set(key, value), add(key, value), mult(key, value).

Se tienen dos métodos remotos: read(key) and update(key, value, operación: set, add, mult). Los resultados para el update son true/false, y para el read el valor de la variable.

La aplicación puede realizarse en cualquier lenguaje de programación.

En proyectos posteriores se deberá tener múltiples servidores que replican el servicio y que deben mantenerse consistentes.
"""

import socket

# Define the server address and port
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 8080

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