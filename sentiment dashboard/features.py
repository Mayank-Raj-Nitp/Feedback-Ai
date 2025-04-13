import requests
from bs4 import BeautifulSoup
import re
import joblib
import numpy as np
import pandas as pd
from data import product_ids
print(product_ids)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Scraping reviews

#Processing the webpage

def scrape_reviews(url, product_id=None, max_reviews=200):
    print("🔍 Starting to scrape reviews...")
    reviews = [] 
    page = 1 
    while len(reviews) < max_reviews:
        print(f"➡️ Fetching page {page}...")
        p_url = f"{url}?page={page}"#Creating a pagnited url to traverse different pages
        response = requests.get(p_url) #Storing the webpage into response variable
        p_code = BeautifulSoup(response.text, 'html.parser') #Using python's HTML parser to split code into useful format

        review_blocks = p_code.select('[data-service-review-text-typography]')
        print(f"✅ Found {len(review_blocks)} reviews on this page.")

        for block in review_blocks:
            text = block.get_text(strip=True)
            reviews.append({
                "product_id": product_id,
                "review": text
            })
            if len(reviews) >= max_reviews:
                break
        page += 1

    print(f"🎯 Total reviews scraped: {len(reviews)}\n")
    return reviews
def preprocess(text):   #corresponding function
    text = text.lower()      #converting all text to lowercase
    text = re.sub(r'[^a-zA-Z\s]', '', text) #removing punctuations and other stuff
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# Load ML model and corresponding vectorizer
print("📦 Loading sentiment model and vectorizer...")
model = joblib.load('model.pkl')       # Loading trained model
vectorizer = joblib.load('vectorizer.pkl')       # Loading the corresponding vectorizer
print("✅ Model and vectorizer loaded!\n")

# Analyzing the pre-processed reviews from earlier
def analyze_reviews(review_objs):
    print("🤖 Running sentiment analysis...")
    texts = [preprocess(r['review']) for r in review_objs]
    X = vectorizer.transform(texts)
    sentiments = model.predict(X)

    for i, r in enumerate(review_objs):
        r['sentiment'] = sentiments[i]
    
    print("📊 Sentiment analysis complete.\n")
    return review_objs

    return sentiments

#  Analytics generation

def generate_analytics(review_objs):
    print("📈 Generating analytics...")
    df = pd.DataFrame(review_objs)
    sentiments = df['sentiment']

    analytics = {
        "total_reviews": len(sentiments),                # Total reviews analyzed
        "positive": int(np.sum(sentiments == 2)),     # Count of positive reviews
        "neutral": int(np.sum(sentiments == 1)),      # Count of neutral reviews
        "negative": int(np.sum(sentiments == 0)),     # Count of negative reviews
        "avg_sentiment_score": float(np.mean(sentiments)), # Average sentiment score
    }

    print("✅ Analytics generated.\n")
    return df, analytics

# Integrating all the functions for scraping 

def integrated_scraping(url):
    reviews = scrape_reviews(url) #scraping from webpage
    sentiments = analyze_reviews(reviews)  #sentiment extraction
    df, analytics = generate_analytics(reviews, sentiments) #analytics generation
    return df, analytics  #returning processed data

inventory = [
    {"product_id": "P101", "name": "iPhone 16"},
    {"product_id": "P102", "name": "iPhone 15"},
    {"product_id": "P102", "name": "iPhone 14"}]


def get_product_id(product_name, inventory):
    for item in inventory:
        if item['name'].lower() in product_name.lower():
            return item['product_id']
    return None

if __name__ == "__main__":
    product_name = "iPhone 16"
    t_url = "https://www.trustpilot.com/review/www.apple.com"

    product_id = get_product_id(product_name, inventory)

    if not product_id:
        print(f"❌ Product '{product_name}' not found in inventory.")
    else:
        print(f"🚀 Scraping reviews for '{product_name}' (ID: {product_id})\n")
        reviews = scrape_reviews(t_url, product_id=product_id)
        enriched_reviews = analyze_reviews(reviews)
        df, analytics = generate_analytics(enriched_reviews)

        print("📋 Sample Reviews with Sentiment:")
        print(df.head(), "\n")

        print("📊 Analytics Summary:")
        for key, value in analytics.items():
            print(f"{key}: {value}")
