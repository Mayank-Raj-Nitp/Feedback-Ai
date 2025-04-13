from flask import Flask, request, jsonify
from db_config import mongo, init_db
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
init_db(app)

@app.route('/reviews/<product_id>', methods=['GET'])
def get_reviews(product_id):
    reviews = list(mongo.db.reviews.find({'product_id': product_id}))
    for r in reviews:
        r['_id'] = str(r['_id'])  # convert ObjectId to string
    return jsonify(reviews), 200

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    if not data or 'product_id' not in data or 'review' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    
    data['created_at'] = datetime.utcnow()  
    mongo.db.reviews.insert_one(data)
    return jsonify({"message": "Review added successfully!"}), 201



if __name__ == '__main__':
    app.run(debug=True)
