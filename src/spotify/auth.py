import os
import requests
from flask import redirect, request, jsonify, session
from urllib.parse import urlencode
from datetime import datetime


##################
## Spotify Auth ##
##################


CLIENT_ID = 'bcf292b2fa9f43fe8d6d8b5824231dcc'
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000/callback'
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

def login():
    scope = 'user-read-private user-read-email user-top-read'
    params = {'client_id': CLIENT_ID, 'response_type': 'code', 'scope': scope, 'redirect_uri': REDIRECT_URI, 'show_dialog': True}
    url = f"{AUTH_URL}?{urlencode(params)}"
    return redirect(url)

def callback():
    error = request.args.get('error')
    code = request.args.get('code')
    if error:
        return jsonify({'error': error})
    if code:
        return exchange_code_for_token(code)
    return jsonify({'error': 'No code provided'})

def exchange_code_for_token(code):
    req_body = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': REDIRECT_URI, 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET}
    response = requests.post(TOKEN_URL, data=req_body)
    if response.status_code != 200:
        return jsonify({'error': 'Failed to retrieve tokens', 'details': response.json()})
    token_info = response.json()
    session.update({'access_token': token_info['access_token'], 'refresh_token': token_info['refresh_token'], 'expires_at': datetime.now().timestamp() + token_info['expires_in']})
    return redirect('/home')