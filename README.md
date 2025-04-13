# 📊 Feedback-Ai – ECommerce Product Sentiment Dashboard

### 🔥 Built at BYTEVERSE 2025

Feedback-Ai is a powerful tool for eCommerce platforms that allows developers to visualize product sentiment using AI-powered review analysis. It combines customer reviews from the platform and social media to deliver actionable insights through a clean desktop dashboard.
---

## 🚀 Features

- 🛍️ **Ecommerce Website** with product listing and review submission -: DEPLOYMENT LINK -: https://myshoppinghub-drab.vercel.app/
- 💬 **User Reviews** stored in MongoDB
- 🤖 **AI-Powered Sentiment Analysis** using Logistic Regression (trained on Amazon Mobile dataset from kaggle)
- 📈 **Aspect-Based Insights**: Price, Battery, Gaming, Build Quality
- 🌐 **Cross-Platform Review Aggregation** (YouTube, Reddit, etc.)
- 📊 **Developer Dashboard App** built in Python (Tkinter + Matplotlib)

---
```
## 🛠️ Tech Stack

| Frontend     | HTML, CSS, JavaScript,ReactJs           |
| Backend      | Python, Flask                           |
| Database     | MongoDB                                 |
| ML Model     | Scikit-learn (Logistic Regression)      |
| ML Libraries | joblib,sklearn, pandas, Matplotlib      |
| GUI Librares | Tkinter                                 |

---
```
## 🧠 How It Works

1. Users submit product reviews on the website.
2. Reviews are stored in MongoDB.
3. Our Python ML model:
   - Converts text to numbers using TF-IDF
   - Predicts sentiment: Positive, Neutral, or Negative
4. Developers can:
   - Select products inside the Python GUI
   - See visual analytics including review breakdown and aspect-based charts
5. External reviews from social platforms are also merged and analyzed.

---

🤖 ML Model Details
🎓 Model: Logistic Regression
We use Logistic Regression trained on the publicly available Amazon Unlocked Mobile dataset from kaggle.
The dataset is preprocessed to remove missing values and convert ratings to sentiments.
---
```
## 📂 Folder Structure
 | Frontend
    |assests
    |index.html
    |product.html
    |script.js
    |styles.css
 | sentiment dashboard
    |db
        |db_config.py
    |model
        |label_encoder.pkl
        |model.pkl
        |vectorizer.pkl
    |utils
         |sentiment_utils.py
    |app.py
    |feature.py
    |data.py
    |requirements.txt
    |seed_data.py
| flask_backend
    |app.py
    |db_config.py
    |requriments.txt
| analysis_model.py
   
---
```
## 🧪 Run Locally

1. **Clone the repo**
git clone https://github.com/Mayank-Raj-Nitp/Feedback-Ai.git
cd Feedback-Ai
2. Install dependencies
   pip install -r requirements.txt
3. Start MongoDB
4. Seed data
   python seed_data.py
5. Run the app
   python app.py

---
📸 Screenshots
![image](https://github.com/user-attachments/assets/44a023f2-53c0-4c7f-864e-876e665dbf70)
![image](https://github.com/user-attachments/assets/b735c9b3-2883-4afe-897f-018970eab21e)

---

🤝 Team members 
1. MAYANK RAJ -: BACKEND & ML
2. ABHIRAJ CHAUDHARY -: ML
3. ANUPAM KUMAR -: FRONTEND




