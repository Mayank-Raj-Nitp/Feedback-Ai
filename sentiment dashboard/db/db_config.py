from pymongo import MongoClient

def get_all_product_ids():
    #connecting with database
    client = MongoClient("mongodb://localhost:27017/")
    database = client["ecommerce"]
    collection = database["reviews"]
    #Take out uniue product ids from reveiws
    return collection.distinct("product_id")

def get_reviews(product_id=None):
    client = MongoClient("mongodb://localhost:27017/")
    database = client["ecommerce"]
    collection = database["reviews"]

    query = {}
    #if product id given
    if product_id:
        query = {"product_id": product_id}
    results = collection.find(query)

#Return review field text 
    reviews = []                     
    for r in results:                
        if 'review' in r:            
            reviews.append(r['review'])  
    return reviews
