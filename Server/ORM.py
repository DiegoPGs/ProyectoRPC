from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from configurations import database_url

# Set up database
engine = create_engine(database_url)
sessionmaker = sessionmaker(bind=engine)
Base = declarative_base()