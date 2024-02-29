import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la ruta de la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(BASE_DIR, 'db.sqlite3')

# Crear el motor de la base de datos
engine = create_engine(f'sqlite:///{db_path}')

# Clase base de SQLAlchemy
Base = declarative_base()

# Definir la tabla de operaciones en una tabla de la base de datos
class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    action = Column(String)
    key = Column(Integer)
    value = Column(Float)

# Crear la tabla en la base de datos
Base.metadata.create_all(engine)
