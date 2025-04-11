from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Create engine
engine = create_engine(
    os.getenv("DB_URL"), echo=True, pool_size=10, max_overflow=20, pool_pre_ping=True
)


def connect_to_database():

    # Creating a Session
    Session = sessionmaker(bind=engine)

    session = Session()

    return session
