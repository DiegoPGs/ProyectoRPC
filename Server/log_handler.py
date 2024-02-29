"""
Productor:  Escucha y Envía mensaje al peer
Consumidor: 
"""
import queue
import threading
from configs import SERVER_PORTS, SERVER_ADDRESS

# Función que esucha mensajes
def escuchar():
    """
    Escucha mensajes del peer en un hilo para ser gestionado en un buffer junto con el hilo que mandará mensajes.
    """
    


def enviar_mensaje():
    """
    Envia mensajes al peer en un hilo para ser gestionado en un buffer junto con el hilo que escucha mensajes.
    """


def main() -> None:
    # Definir el buffer intermedio con capacidad de 7 elementos
    buffer = queue.Queue(maxsize=7)

    # Crear hilos para los productores y el consumidor
    threads = []
    producer_thread = threading.Thread(target=escuchar)
    consumer_thread = threading.Thread(target=enviar_mensaje)

    # Agregar los hilos a la lista
    threads.append(producer_thread)
    threads.append(consumer_thread)

    # Iniciar los hilos
    for thread in threads:
        thread.start()
    
    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    consumer_thread.join()


if __name__ == '__main__':
    main()
