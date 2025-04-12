from pymongo import MongoClient

sample_reviews = [
    {"product_id": "P101", "review": "Battery life is amazing"},
    {"product_id": "P101", "review": "Great for gaming, no lag"},
    {"product_id": "P101", "review": "Great pricing"},
    {"product_id": "P102", "review": "Cheap plastic build"},
    {"product_id": "P102", "review": "Design is solid and premium"},
    {"product_id": "P102", "review": "Battery life is okay"},
    {"product_id": "P103", "review": "Battery life is amazing"},
    {"product_id": "P103", "review": "Great for gaming, no lag"},
    {"product_id": "P103", "review": "Great pricing "},
    {"product_id": "P104", "review": "Cheap plastic build"},
    {"product_id": "P104", "review": "Design is solid and premium"},
    {"product_id": "P104", "review": "Battery life is okay"},
    {"product_id": "P105", "review": "Battery life is amazing"},
    {"product_id": "P105", "review": "Great for gaming, no lag"},
    {"product_id": "P105", "review": "Great Pricing "},
    {"product_id": "P106", "review": "Cheap plastic build"},
    {"product_id": "P106", "review": "Design is solid and premium"},
    {"product_id": "P106", "review": "Battery life is okay"},
    {"product_id": "P107", "review": "Battery life is amazing"},
    {"product_id": "P107", "review": "Great for gaming, no lag"},
    {"product_id": "P107", "review": "Great pricing"},
    {"product_id": "P108", "review": "Cheap plastic build"},
    {"product_id": "P108", "review": "Design is solid and premium"},
    {"product_id": "P108", "review": "Battery life is okay"},
    

]

client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
collection = db["reviews"]
collection.insert_many(sample_reviews)
print("✅ Sample reviews added!")
