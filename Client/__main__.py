import json
from client import Client
from configs import SERVER_ADDRESS, SERVER_PORT

def main():
    # Create the client
    client = Client(SERVER_ADDRESS, SERVER_PORT)

    # Define the data to send to the server
    data = [
        {'key': 0, 'value': 10.1, 'operation': 'set'},
        {'key': 0, 'value': 10.1, 'operation': 'add'},
        {'key': 1, 'value': 10.1, 'operation': 'set'}
    ]

    for d in data:
        # Serialize the data
        d = json.dumps(d)

        # Send a request to the server
        response = client.send_request(d)

        print(f"Response: {response}")

if __name__ == '__main__':
    main()