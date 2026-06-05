from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["electronics"]

products = [
    {
        "name": "Samsung Galaxy S24",
        "category": "Mobile",
        "price": 999,
        "description": "Latest Samsung flagship with 6.2 inch display and 50MP camera.",
        "image": "https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400",
        "stock": 10
    },
    {
        "name": "Apple MacBook Air M2",
        "category": "Laptop",
        "price": 1299,
        "description": "Thin and powerful laptop with Apple M2 chip and 13 inch display.",
        "image": "https://images.unsplash.com/photo-1611186871525-964d04b4a2ce?w=400",
        "stock": 5
    },
    {
        "name": "Sony WH-1000XM5",
        "category": "Headphones",
        "price": 349,
        "description": "Industry leading noise cancelling wireless headphones.",
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        "stock": 15
    },
    {
        "name": "iPad Pro 12.9",
        "category": "Tablet",
        "price": 1099,
        "description": "Powerful tablet with M2 chip and stunning Liquid Retina display.",
        "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",
        "stock": 8
    },
    {
        "name": "Dell Monitor 27 inch",
        "category": "Monitor",
        "price": 399,
        "description": "4K UHD monitor with USB-C connectivity and slim bezels.",
        "image": "https://images.unsplash.com/photo-1527443224154-c4a573d5e189?w=400",
        "stock": 12
    },
    {
        "name": "Logitech MX Master 3",
        "category": "Accessories",
        "price": 99,
        "description": "Advanced wireless mouse with ergonomic design for productivity.",
        "image": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",
        "stock": 20
    },
    {
        "name": "Apple iPhone 15 Pro",
        "category": "Mobile",
        "price": 1199,
        "description": "iPhone 15 Pro with titanium design and A17 Pro chip.",
        "image": "https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400",
        "stock": 7
    },
    {
        "name": "HP Pavilion Laptop 15",
        "category": "Laptop",
        "price": 749,
        "description": "Everyday laptop with Intel Core i5 and 8GB RAM.",
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400",
        "stock": 9
    }
]

db.products.drop()
db.products.insert_many(products)
print(f"Inserted {len(products)} products successfully!")