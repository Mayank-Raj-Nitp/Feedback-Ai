#using joblib library for loading pre-trained model
import joblib

# Loding the artifacts of the model
model = joblib.load("model/model.pkl") #Loading the ML model
vectorizer = joblib.load("model/vectorizer.pkl") #Loading the numerical values of text that were assigned to data used for training
label_encoder = joblib.load("model/label_encoder.pkl") #Loading the mapping of Labels 

# Providing a dictionary containing keywords that would help in judgement of a parameter 
aspects_keywords = {
    "Pricing": ["price", "expensive", "cheap", "value", "cost"],
    "Build Quality": ["build", "material", "design", "durable"],
    "Gaming": ["gaming", "lag", "fps", "performance"],
    "Battery": ["battery", "charging", "power", "backup", "life"]
}

#for classifiying the feedback reviews based on the sentiments being reflected
def classify_sentiments(reviews):
    predictions = model.predict(vectorizer.transform(reviews))  #conversion for text to number in IT-IDF
    sentiments = label_encoder.inverse_transform(predictions)
    return list(zip(reviews, sentiments)) #returning the reviews with corresponding predicted sentiment

# analyzing the code for aspects_keywords

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

    return average #returning the average
