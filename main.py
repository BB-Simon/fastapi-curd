from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get('/')
def sayHi():
  return 'Hello, this is Simon from FastAPI'


products = [
  Product(id=1, name='Productc #1', description='Product #1 description', price=12, quantity=20),
  Product(id=2, name='Productc #2', description='Product #2 description', price=2, quantity=20),
]

@app.get('/api/products')
def getProducts():
  return products

@app.get('/api/product/{id}')
def get_product(id: int):
  for product in products:
    if product.id == id:
      return product
    
    return 'Product not found'
  

@app.post('/api/product')
def add_product():
  products.append(
      Product(id=3, name='Productc #3',
              description='Product #3 description', price=2, quantity=20)
  )