import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Loading the CSV file containg feedback data into pandas dataframe for training and testing
df = pd.read_csv("Amazon_UnlocKed_Mobile.csv") 



# Data cleaning
df = df.dropna(subset=['Reviews', 'Rating'])

# Converting feedback rating into string 

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

#Performing the conversion and saving new data 

df['Sentiment'] = df['Rating'].apply(rating_to_sentiment)
df = df.dropna(subset=['Sentiment']) #Removing row where conversion fails 

# Defining Features and Labels
X = df['Reviews']
y = df['Sentiment'] 


vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
vectorizer.fit(X)  # Learn vocabulary and IDF
X_tfidf = vectorizer.transform(X) 
# Fit the label encoder to learn the mapping
label_encoder = LabelEncoder()
label_encoder.fit(y)

# Transform the labels into numerical values
y_encoded = label_encoder.transform(y) # negative:0, neutral:1, positive:2

# Splitting the data for testing and training purpose

   #X_train: TF-IDF features for training the model.
   #X_test: TF-IDF features for testing the model.
   #y_train: Encoded labels corresponding to X_train.
   #y_test: Encoded labels corresponding to X_test.

X_train, X_test, y_train, y_test = train_test_split( 
    X_tfidf, y_encoded, test_size=0.2, random_state=42) #test_size specifies 20% data for testing purpose 
                                                        #random_state ensures there that model maintains same state every time it is compiled
# Training the model using LogisticRegression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluating the model after learning
y_pred = model.predict(X_test)

print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:")
print(classification_report(
    y_test,
    y_pred,
    labels=[0, 1, 2],
    target_names=label_encoder.classes_
))

#For testing new feedback in the model

test_review = "Battery is very good"  # Providing feedback statement 
test_vector = vectorizer.transform([test_review]) 
prediction = model.predict(test_vector)
sentiment = label_encoder.inverse_transform(prediction)[0]
print(f"\n🔮 New review prediction: '{test_review}' → {sentiment}")

#For saving the trained model and the componenets to disk

joblib.dump(model, "model.pkl")  #For storing learned parameters in order to load them later
joblib.dump(vectorizer, "vectorizer.pkl")  #For storing the learned vocabulary and IDF values for transforming new text in similar way as used for learning 
joblib.dump(label_encoder, "label_encoder.pkl") #for storing relation between the present labels in the model {(positive:2)(negative:0)(neutral:0)}
