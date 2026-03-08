import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://car_rental_db_6sv4_user:ESli87WO1FArjhxXicBerwT2ZGmBpdfr@dpg-d6mmc5fafjfc7397ensg-a.oregon-postgres.render.com/car_rental_db_6sv4"
)

if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL

)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

Base = declarative_base()