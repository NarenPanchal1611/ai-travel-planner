# 🌍 AI-Powered Travel Planner

An intelligent travel planning web application that recommends destinations based on user preferences using Machine Learning.

---

## 🚀 Features

- 🔐 User Authentication (Login / Signup)
- 🧠 ML-based Recommendation System (TF-IDF + Cosine Similarity)
- 💰 Budget-based Filtering
- 📊 CSV-based scalable dataset
- 📝 Login History Tracking (Admin feature)

---

## 🛠️ Tech Stack

- **Backend:** Flask
- **Machine Learning:** scikit-learn
- **Database:** SQLite (users.db)
- **Data Handling:** pandas
- **Deployment:** Gunicorn + Render
- **Frontend:** HTML + CSS

---

## 🧠 How It Works

1. User enters:
   - Destination location
   - Budget
   - Interests (e.g., beach, mountains)

2. System:
   - Converts text input into vectors using TF-IDF
   - Calculates similarity with destination dataset
   - Filters results based on budget
   - Returns top recommended places

---

## 📁 Project Structure