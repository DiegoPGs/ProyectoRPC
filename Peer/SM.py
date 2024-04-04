import logging

# Set up logger
logging.basicConfig(filename='logs.log', level=logging.INFO)

class StateMachine:
    def __init__(self):
        # dictionary of states
        self.data = {}
        # logging
        logging.info(f'[StateMachine] StateMachine initialized with data {self.data} and obj_id {id(self)}')
    
    # contador de lamport
    count : int = 0

    def __del__(self):
        # logging
        logging.info(f'[StateMachine] StateMachine deleted with data {self.data} and obj_id {id(self)}')

    # methods
    def transition(self, data):
        """
        Transitions the state machine

        Args:
            data (string): data to transition the state machine

        Returns:
            Bool: response from the state machine
        """
        print(f'Data received: {data}')

        try:
            # string to dictionary
            data = eval(data)
            # get key and value
            key = data.get('key')
            value = data.get('value')
            if data.get('action') is None:
                # read operation
                return self.get(key)
            else:
                # update operation
                operation = data.get('action')
                return self.update(key, value, operation)
        except Exception as e:
            print(f'[StateMachine] Error: {e}')
            logging.error(f'[StateMachine] Error: {e}')
            return False

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

    def update(self, key, value, action):
        """
        Método remoto para actualizar el valor de una clave.
        Similar a RMI en Java.

        Args:
            key (int): clave a actualizar
            value (float): valor a actualizar
            action (str): operación a realizar

        Returns:
            bool: True si la operación se realizó correctamente, False en caso contrario
        """
        actions = {
            'set': self.set,
            'add': self.add,
            'mult': self.mult
        }
        accion = actions.get(action)

        if accion:
            logging.info(f'[StateMachine] action {action} and value {value}') 
            accion(key, value)
            logging.info(f'[StateMachine] Key {key} updated to {self.get(key)}')
            return True
        else:
            print(f'Invalid action: {action}')
            return False

    def exportar(self):
        """
        Exporta la máquina de estados a un diccionario de datos.

        Returns:
            dict: diccionario de datos exportado
        """
        logging.info(f'[StateMachine] Exported StateMachine\tobj_id {id(self)}')
        return self.data

    def importar(self, data):
        """
        Importa un diccionario de datos a la máquina de estados.

        Args:
            data (dict): diccionario de datos a importar
        """
        logging.info(f'[StateMachine] Imported StateMachine\tobj_id {id(self)}')
        self.data = data

    def copiar(self):
        """
        Copia la máquina de estados.

        Returns:
            StateMachine: copia de la máquina de estados
        """
        logging.info(f'[StateMachine] Copied StateMachine\tobj_id {id(self)}')
        sm = StateMachine()
        sm.importar(self.exportar())
        return sm
