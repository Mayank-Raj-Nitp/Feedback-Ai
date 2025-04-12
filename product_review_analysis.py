import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Step 1: Load CSV
df = pd.read_csv("Amazon_UnlocKed_Mobile.csv")  # Replace with actual filename

# Step 2: Drop rows with missing reviews or ratings
df = df.dropna(subset=['Reviews', 'Rating'])

# Step 3: Convert rating to sentiment
def rating_to_sentiment(rating):
    try:
        rating = float(rating)
    except:
        return None
    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"

df['Sentiment'] = df['Rating'].apply(rating_to_sentiment)
df = df.dropna(subset=['Sentiment'])  # Drop if conversion failed

# Step 4: Features and Labels
X = df['Reviews']
y = df['Sentiment']

# Step 5: Text to numbers (TF-IDF)
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_tfidf = vectorizer.fit_transform(X)

# Step 6: Encode labels (text -> number)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)  # negative:0, neutral:1, positive:2

# Step 7: Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y_encoded, test_size=0.2, random_state=42
)

# Step 8: Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Step 9: Evaluate
y_pred = model.predict(X_test)

print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:")
print(classification_report(
    y_test,
    y_pred,
    labels=[0, 1, 2],
    target_names=label_encoder.classes_
))

# Step 10: Try a new review
test_review = "Battery is very good"
test_vector = vectorizer.transform([test_review])
prediction = model.predict(test_vector)
sentiment = label_encoder.inverse_transform(prediction)[0]
print(f"\n🔮 New review prediction: '{test_review}' → {sentiment}")

# After training
joblib.dump(model, "model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
