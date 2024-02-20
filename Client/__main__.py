import threading
import json
from client import Client
from configs import SERVER_ADDRESS, SERVER_PORT

def send_request(data):
    client = Client(SERVER_ADDRESS, SERVER_PORT)
    response = client.send_request(data)
    print(f"Response: {response}")

def main():
    # Define the data to send to the server
    data = [
        {'key': 0, 'value': 10.13, 'operation': 'set'},
        {'key': 0, 'value': 10.12, 'operation': 'add'},
        {'key': 1, 'value': 10.1, 'operation': 'set'},
        {'key': 1, 'value': 10.0, 'operation': 'add'},
        {'key': 2, 'value': 10.1, 'operation': 'set'},
        {'key': 0, 'value': 10.8, 'operation': 'add'},
        {'key': 3, 'value': 10.7, 'operation': 'set'},
        {'key': 0, 'value': 10.6, 'operation': 'add'},
        {'key': 0, 'value': 10.5, 'operation': 'set'},
        {'key': 1, 'value': 10.3, 'operation': 'add'},
        {'key': 3, 'value': 10.2, 'operation': 'set'}
    ]

    threads = []
    for d in data:
        # Serialize the data
        d = json.dumps(d)
        thread = threading.Thread(target=send_request, args=(d,))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
