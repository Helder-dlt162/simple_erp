from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import db_config


engine = create_engine(db_config["DB_URL"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)