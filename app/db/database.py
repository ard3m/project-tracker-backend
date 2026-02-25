# app/db/database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Naming convention for Alembic-friendly constraint names
naming_convention = {
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}
metadata = MetaData(naming_convention=naming_convention)

class Base(DeclarativeBase):
    metadata = metadata

DATABASE_URL = "postgresql+psycopg2://user:pass@localhost:5432/yourdb"
engine = create_engine(DATABASE_URL, echo=False, future=True, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)