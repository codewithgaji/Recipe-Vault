from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()


db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL Not Set")

# This is a conditional statement to confirm db_url
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)



engine = create_engine(db_url) # This is used to create a connection to the database using the URL provided in the environment variable. The create_engine function is from SQLAlchemy and it takes the database URL as an argument. It returns an Engine object that can be used to interact with the database.
          
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

