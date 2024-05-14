from flask import Flask, render_template, session, redirect
import os
from dotenv import load_dotenv

from spotify.auth import login, callback
from recommendation_engine.recommender import get_recommendations

##################
## Flask Routes ##
##################

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise ValueError("No secret key set for Flask application")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_route():
    return login()

@app.route('/callback')
def callback_route():
    return callback()

@app.route('/home')
def home():
    recommendations = get_recommendations()

    print(recommendations)
    
    if recommendations is None: return render_template('profile.html', error="Access token is not available. Please log in.")

    return render_template('profile.html', recommendations=recommendations, explanations="", error=None)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)