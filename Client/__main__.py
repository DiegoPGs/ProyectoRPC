import threading
import json
from client import Client
from configs import SERVER_ADDRESS, SERVER_PORT

def send_request(data):
    client = Client(SERVER_ADDRESS, SERVER_PORT)
    response = client.send_request(data)

def main():
    # Define the data to send to the server
    data = [
        {'key': 0, 'value': 10.13, 'action': 'set'}
    ]

    """
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
    """
    for d in data:
        # Serialize the data
        d = json.dumps(d)
        send_request(d)

if __name__ == '__main__':
    main()
