import asyncio
#import icecream as ic


class StateMachine:
    def __init__(self):
        # dictionary of states
        self.data = {}

    # public methods
    def get(self, key):
        """
        Getter for data dictionary

        Args:
            key (dictionary key): for data dictionary

        Returns:
            _type_: value of data[key]
        """
        return self.data.get(key)

    def set(self, key, value):
        """
        Setter for data dictionary

        Args:
            key (dictionary key): position to modify
            value (_type_): value to be set
        """
        self.data[key] = value

    def add(self, key, value):
        """
        Adds value to data[key]

        Args:
            key (int): position to modify
            value (float): value to be added
        """
        if key in self.data:
            self.data[key] += value
        else:
            self.data[key] = value

    def mult(self, key, value):
        """
        Multiplies value to data[key]

        Args:
            key (int): position to modify
            value (float): value to be multiplied
        """
        if key in self.data:
            self.data[key] *= value
        else:
            self.data[key] = 0

    # remote methods
    def read(self, key):
        """
        Método remoto para leer el valor de una clave.
        Similar a RMI en Java.

        Args:
            key (int): clave a leer
        """
        return self.get(key)

    def update(self, key, value, operation):
        """
        Método remoto para actualizar el valor de una clave.
        Similar a RMI en Java.

        Args:
            key (int): clave a actualizar
            value (float): valor a actualizar
            operation (str): operación a realizar

        Returns:
            bool: True si la operación se realizó correctamente, False en caso contrario
        """
        actions = {
            'set': self.set,
            'add': self.add,
            'mult': self.mult
        }
        action = actions.get(operation)

        if action:
            action(key, value)
            return True
        else:
            print(f'Invalid operation: {operation}')
            return False
