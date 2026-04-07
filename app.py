from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
app.secret_key = "your_secret_key_123"

# ------------------ DATABASE SETUP ------------------
def init_db():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ------------------ HOME ------------------
@app.route('/')
def home():
    return render_template('index.html')

# ------------------ SIGNUP ------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "⚠️ Email already exists!"

        conn.close()
        return redirect('/login')

    return render_template('signup.html')

# ------------------ LOGIN ------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect('/dashboard')
        else:
            return "❌ Invalid email or password"

    return render_template('login.html')

# ------------------ DASHBOARD ------------------
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['username'])

# ------------------ PLANNER ------------------

@app.route('/planner', methods=['GET', 'POST'])
def planner():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        budget = int(request.form['budget'])
        days = int(request.form['days'])
        user_input = request.form['interests']

        # 🔥 Load dataset
        data = pd.read_csv('places.csv')

        place_names = data['name'].tolist()
        place_features = data['features'].tolist()
        place_costs = data['cost'].tolist()

        # 🔥 ML (TF-IDF)
        all_data = place_features + [user_input]

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(all_data)

        similarity = cosine_similarity(vectors[-1], vectors[:-1])

        scores = list(enumerate(similarity[0]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        # 🔥 Recommendation + Budget Filter
        recommendations = []

        for i in scores:
            index = i[0]

            if place_costs[index] <= budget:
                recommendations.append(place_names[index])

            if len(recommendations) == 3:
                break

        # 🔥 Itinerary Generator
        itinerary = []

        for i in range(days):
            place = recommendations[i % len(recommendations)]
            itinerary.append(f"Day {i+1} → Visit {place}")

        return render_template(
            'result.html',
            places=recommendations,
            itinerary=itinerary,
            days=days,
            budget=budget
        )

    return render_template('planner.html')
# ------------------ LOGOUT ------------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ------------------ RUN ------------------
if __name__ == '__main__':
    app.run(debug=True)