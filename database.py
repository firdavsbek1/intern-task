from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_PASSWORD=''
DB_USER=''

engine=create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost/records",echo=True)
SessionLocal=sessionmaker()
Base=declarative_base()