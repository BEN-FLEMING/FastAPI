#to handle databse connection
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency every time we get request - we open a session and then close it out - this is much more efficient 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()