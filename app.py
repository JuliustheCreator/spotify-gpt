from flask import Flask, request, render_template, redirect, jsonify, session
import os
from dotenv import load_dotenv
import openai
import json
import requests
import datetime
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import parse_qs



load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise ValueError("No secret key set for Flask application")

openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("No OpenAI API key set")

CLIENT_ID = 'bcf292b2fa9f43fe8d6d8b5824231dcc'
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
if not CLIENT_SECRET:
    raise ValueError("No Spotify client secret set")

REDIRECT_URI = 'http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return "Welcome to the XAI Music Recommender <a href='/login'>Click here to get started</a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': REDIRECT_URI,
        'show_dialog': True
    }

    url = f"{AUTH_URL}?{urlencode(params)}"
    return redirect(url)

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({'error': request.args['error']})
    
    if 'code' in request.args:
        req_body = {
            'grant_type': 'authorization_code',
            'code': request.args['code'],
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    
        response = requests.post(TOKEN_URL, data=req_body)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to retrieve tokens', 'details': response.json()})
        
        token_info = response.json()

        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']

        return redirect('/home')
    return jsonify({'error': 'Authorization failed. No code provided.'})



@app.route("/playlists")
def get_playlists():
    if 'access_token' not in session:
        return redirect('/login')
    
    if datetime.datetime.now() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(f"{API_BASE_URL}me/playlists", headers=headers)
    playlists = response.json()

    return jsonify(playlists)


@app.route("/refresh-token")
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
    
    response = requests.post(TOKEN_URL, data=req_body)
    token_info = response.json()

    session['access_token'] = token_info['access_token']
    session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']

    return redirect('/home')

@app.route("/home", methods=["GET", "POST"])
def home():
    recommendations = ""
    x = 10
    if request.method == "POST":
        songs_json = request.form.get("songs")
        if songs_json:
            songs = json.loads(songs_json)
            prompt = f'''
            List {x} lesser-known artists for someone with the following song preferences. Prioritize uniqueness and obscurity in your recommendations:\n
            {songs}
            '''

            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music recommender system, with a deep understanding of modern music and pop culture. You will recommend artists to the users, you should say absolutely nothing else but each artist's names seperated by new lines."},
                {"role": "user", "content": prompt}
            ]
            )
            recommendations = (completion.choices[0].message)['content'].split('\n')

    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

