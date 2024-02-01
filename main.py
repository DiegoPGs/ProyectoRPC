import logging
import random as r
from Server import StateMachineServer
from Server.server import SERVER_ADDRESS, SERVER_PORT

# Set up logger 
logging.basicConfig(filename='logs.log', level=logging.INFO)

def main():
    # Create the server
    with StateMachineServer(SERVER_ADDRESS, SERVER_PORT) as server:
        # Start the server
        server.start()

        # Log the server start
        logging.info(f'Server started on {SERVER_ADDRESS}:{SERVER_PORT}')

        clients = 3
        for i in range(clients):
            # Log the client connection
            logging.info(f'Client {i} connected')

            data = {
                'key': i,
                'value': 10,
                'operation': 'set'
            }

            data = {
                'key': i,
                'value': 10,
                'operation': 'add' if r.random() > 0.5 else 'mult'
            }

            # Log the client request
            logging.info(f'Client {i} request: Hello, server! uwuw')

            # Log the server response
            logging.info(f'Server response: Hello, client {i}! uwuw')

    # Start the server
    server.start()



if __name__ == '__main__':
    main()
