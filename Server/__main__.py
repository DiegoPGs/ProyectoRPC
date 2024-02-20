from cserver import ConcurrentStateMachineServer
from server import SERVER_ADDRESS, SERVER_PORT


def main():
    server = ConcurrentStateMachineServer(SERVER_ADDRESS, SERVER_PORT)
    server.start()

if __name__ == '__main__':
    main()
