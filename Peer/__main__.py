from peer import Peer
from server import SERVER_ADDRESS, SERVER_PORT
from configs import SERVER_ADDRESS, SERVER_PORTS


def main() -> None:
    server = Peer(SERVER_ADDRESS, SERVER_PORT)
    server.start()

if __name__ == '__main__':
    main()
