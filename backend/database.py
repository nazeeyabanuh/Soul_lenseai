from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///soullens.db",
    echo=True
)

SessionLocal = sessionmaker(
    bind=engine
)