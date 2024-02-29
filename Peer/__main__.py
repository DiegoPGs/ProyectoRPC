import threading
from peer import Peer
from server import SERVER_ADDRESS, SERVER_PORT
from configs import SERVER_ADDRESS, SERVER_PORTS


def main() -> None:
    threads = []
    for p in SERVER_PORTS:
        peer = Peer(SERVER_ADDRESS, p)
        thread = threading.Thread(target=peer.start)
        thread.start()
        threads.append(thread)

if __name__ == '__main__':
    main()
