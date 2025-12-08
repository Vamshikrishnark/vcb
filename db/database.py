import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql://postgres:root@localhost:5432/testdb")

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
