from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Database connection
def get_db():
    conn = sqlite3.connect('itech.db')
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic models
class Product(BaseModel):
    name: str
    type: str
    buying_price: float
    selling_price: float

class Service(BaseModel):
    name: str
    description: str
    price: float

class Stock(BaseModel):
    product_name: str
    quantity: int
    price_per_unit: float

# Create tables
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            buying_price REAL NOT NULL,
            selling_price REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit REAL NOT NULL
        )
    ''')
    conn.commit()

# Initialize the database
init_db()

# Product endpoints
@app.post("/products/")
def add_product(product: Product):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (name, type, buying_price, selling_price)
        VALUES (?, ?, ?, ?)
    ''', (product.name, product.type, product.buying_price, product.selling_price))
    conn.commit()
    return {"message": "Product added successfully"}

@app.get("/products/")
def get_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    return {"products": products}

# Service endpoints
@app.post("/services/")
def add_service(service: Service):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO services (name, description, price)
        VALUES (?, ?, ?)
    ''', (service.name, service.description, service.price))
    conn.commit()
    return {"message": "Service added successfully"}

@app.get("/services/")
def get_services():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM services')
    services = cursor.fetchall()
    return {"services": services}

# Stock endpoints
@app.post("/stock/")
def add_stock(stock: Stock):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO stock (product_name, quantity, price_per_unit)
        VALUES (?, ?, ?)
    ''', (stock.product_name, stock.quantity, stock.price_per_unit))
    conn.commit()
    return {"message": "Stock added successfully"}

@app.get("/stock/")
def get_stock():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stock')
    stock = cursor.fetchall()
    return {"stock": stock}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
