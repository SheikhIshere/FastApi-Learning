from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engin = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engin)

Base = declarative_base()

"""

Base = declarative_base() creates a declarative base class that serves as the foundation for all your SQLAlchemy ORM models.

What it represents:
Base: A base class that all your database models will inherit from
declarative_base(): SQLAlchemy function that creates a special class with ORM capabilities
What it enables:
When you define models like Todos(Base), the Base class provides:

Table mapping: Automatically maps Python classes to database tables
Column definitions: Allows Column() objects to define table fields
Metadata tracking: Collects all table definitions for schema creation
ORM functionality: Enables

"""