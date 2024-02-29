import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from generate_db import Operation

# Definir la ruta de la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, 'db.sqlite3')

# Crear el motor y la sesión de la base de datos
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
session = Session()

class OperationsFramework:
    def create(self, action, key, value):
        """Crear una nueva operación."""
        operation = Operation(action=action, key=key, value=value)
        session.add(operation)
        session.commit()

    def read(self, key):
        """Leer una operación por su clave."""
        operation = session.query(Operation).filter_by(key=key).first()
        if operation:
            return {'action': operation.action, 'key': operation.key, 'value': operation.value}
        else:
            return None

    def update(self, key, action=None, value=None):
        """Actualizar una operación por su clave."""
        operation = session.query(Operation).filter_by(key=key).first()
        if operation:
            if action:
                operation.action = action
            if value:
                operation.value = value
            session.commit()
            return True
        else:
            return False

# Ejemplo de uso
def main() -> None:
    framework = OperationsFramework()
    # Leer la operación con clave 1
    print(framework.read(1))
    # Actualizar la operación con clave 1
    framework.update(1, action='new_action', value=123.45)

if __name__ == '__main__':
    main()
