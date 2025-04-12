import joblib

# Load model artifacts
model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

# Aspect keywords
aspects_keywords = {
    "Pricing": ["price", "expensive", "cheap", "value", "cost"],
    "Build Quality": ["build", "material", "design", "durable"],
    "Gaming": ["gaming", "lag", "fps", "performance"],
    "Battery": ["battery", "charging", "power", "backup", "life"]
}

def classify_sentiments(reviews):
    predictions = model.predict(vectorizer.transform(reviews))
    sentiments = label_encoder.inverse_transform(predictions)
    return list(zip(reviews, sentiments))

def get_aspect_sentiments(reviews):
    aspect_scores = {k: [] for k in aspects_keywords}

    for review in reviews:
        sentiment_num = model.predict(vectorizer.transform([review]))[0]
        for aspect, keywords in aspects_keywords.items():
            if any(word in review.lower() for word in keywords):
                aspect_scores[aspect].append(sentiment_num)

    # Average sentiment for each aspect
    average = {
        aspect: round(sum(scores) / len(scores), 2) if scores else None
        for aspect, scores in aspect_scores.items()
    }

    return average
