from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
import os

Base = declarative_base()
metadata = MetaData()

database_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/db')
engine = create_engine(database_url, echo=True)
session = Session(engine)

session.execute(text('CREATE EXTENSION IF NOT EXISTS vector'))
session.commit()

print("Extension created")
