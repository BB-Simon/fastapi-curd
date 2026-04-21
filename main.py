from fastapi import FastAPI, Depends
from models import Product
from database import session, engine

import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)

@app.get('/')
def sayHi():
  return 'Hello, this is Simon from FastAPI'


products = [
  Product(id=1, name='Productc #1', description='Product #1 description', price=12, quantity=20),
  Product(id=2, name='Productc #2', description='Product #2 description', price=2, quantity=20),
]

def get_db():
  db = session()
  try:
    yield db
  finally:
    db.close()


def init_db():
  db = session()
  count = db.query(database_models.Product).count
  if(count == 0):
    for product in products:
      db.add(database_models.Product(**product.model_dump()))
  
  db.commit()


init_db()

@app.get('/api/products')
def getProducts(db: Session = Depends(get_db)):
  db_products = db.query(database_models.Product).all()
  return db_products

@app.get('/api/product/{id}')
def get_product(id: int, db: Session = Depends(get_db)):
  db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
  if db_product:
    return db_product
    
  return 'Product not found'
  

@app.post('/api/product')
def add_product(product: Product, db: Session = Depends(get_db)):
  db.add(database_models.Product(**product.model_dump()))
  db.commit()
  return product

@app.put('/api/product')
def add_product(id: int, product: Product, db: Session = Depends(get_db)):
  db_product = db.query(database_models.Product).filter(
      database_models.Product.id == id).first()
  if db_product:
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    db.commit()
    return 'Product updated successfully'

  return 'Product not found'

@app.delete('/api/product')
def add_product(id: int, db: Session = Depends(get_db)):
  db_product = db.query(database_models.Product).filter(
      database_models.Product.id == id).first()
  if db_product:
    db.delete(db_product)
    db.commit()
    return 'Product deleted successfully'

  return 'Product not found'
