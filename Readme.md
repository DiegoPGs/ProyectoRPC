### Primer pryecto de sistemas distribuidos
# Proyecto RPC
## Alumnos: Diego Ignacio Puente Gallegos, Jesús 

#### Instrucciones de proyecto
En el primer proyecto se solicita programar una aplicación usando RPC (RMI). Se debe contar con varios clientes que envían solicitudes a un servidor.

El servidor debe tener una máquina de estado (SM) muy sencilla que ejecute las solicitudes de los clientes.

(Schneider, 1990) “A state machine consists of state variables, which encode its state, and commands, which transform its state. Each command is implemented by a deterministic program; execution of the command modifies the state variables and/or produces some output. The defining characteristic of a state machine is that it specifies a deterministic computation that reads a stream of requests and processes each, occasionally producing output.”

De las operaciones CRUD nos quedaremos solo con Read y Update (solo podremos, después, leer y modificar un campo de un registro de una tabla de la base de datos).

Modelamos el estado de la SM con un objeto. El objeto tiene un diccionario que almacena valores reales y métodos (comandos) públicos get(key), set(key, value), add(key, value), mult(key, value).

Se tienen dos métodos remotos: read(key) and update(key, value, operación: set, add, mult). Los resultados para el update son true/false, y para el read el valor de la variable.

La aplicación puede realizarse en cualquier lenguaje de programación.

En proyectos posteriores se deberá tener múltiples servidores que replican el servicio y que deben mantenerse consistentes.


#### Instruciones para correr proyecto
pip install requirements.txt

python Server
python client.py

Ejecutar client.py para cada operación.