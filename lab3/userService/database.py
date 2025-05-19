from models import  DbUser, Base
from passlib.hash import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Настройка SQLAlchemy
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db/postgres")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if not db.query(DbUser).filter_by(username="admin").first():
        admin_user = DbUser(
            username="admin",
            password_hash=bcrypt.hash("secret")
        )
        db.add(admin_user)
        db.commit()

    db.close()