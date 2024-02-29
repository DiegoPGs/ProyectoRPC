import threading
import queue
import time
import random

# Definir el buffer intermedio con capacidad de 7 elementos
buffer = queue.Queue(maxsize=7)

# Función que simula la tarea del productor
def producer_task(producer_id):
    for _ in range(10):  # Produce 10 elementos
        item = random.randint(1, 100)
        
        # Intenta poner el elemento en el buffer
        try:
            buffer.put(item, block=True, timeout=1)
            print(f"Productor {producer_id}: Produjo elemento {item}")
        except queue.Full:
            print(f"Productor {producer_id}: Buffer lleno, esperando")

        # Simula alguna operación antes de producir el siguiente elemento
        time.sleep(random.uniform(1, 5))

# Función que simula la tarea del consumidor
def consumer_task():
    for _ in range(20):  # Consume 20 elementos
        # Intenta obtener un elemento del buffer
        try:
            item = buffer.get(block=True, timeout=1)
            print(f"Consumidor: Consumió elemento {item}")
        except queue.Empty:
            print("Consumidor: Buffer vacío, esperando")

        # Simula alguna operación antes de consumir el siguiente elemento
        time.sleep(random.uniform(0.1, 0.5))

# Crear hilos para los productores y el consumidor
producer_threads = []
for i in range(2):
    thread = threading.Thread(target=producer_task, args=(i,))
    producer_threads.append(thread)

consumer_thread = threading.Thread(target=consumer_task)

# Iniciar los hilos
for thread in producer_threads:
    thread.start()

consumer_thread.start()

# Esperar a que todos los hilos terminen
for thread in producer_threads:
    thread.join()

consumer_thread.join()

print("Todas las tareas han sido completadas.")
