from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:123$$$sss@localhost:5432/fastapi-curd"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False, bind=engine)