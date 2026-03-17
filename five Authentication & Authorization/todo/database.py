from  sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# sqlite configuration
# SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db" 
SQLALCHEMY_DATABASE_URL = "postgresql://fastapi_user:password@localhost:5432/todoapp"

# engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}) # this is for sqllite only
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


