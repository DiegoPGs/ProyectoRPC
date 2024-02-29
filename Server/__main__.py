import threading
from cserver import ConcurrentStateMachineServer
from server import SERVER_ADDRESS, SERVER_PORT
from configs import SERVER_ADDRESS, SERVER_PORTS


def main():
    threads = []
    for port in SERVER_PORTS:
        server = ConcurrentStateMachineServer(SERVER_ADDRESS, port)
        thread = threading.Thread(target=server.start)
        thread.start()
        threads.append(thread)
    #server = ConcurrentStateMachineServer(SERVER_ADDRESS, SERVER_PORT)
    #server.start()

if __name__ == '__main__':
    main()
