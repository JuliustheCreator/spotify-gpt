import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def authenticate_spotify():
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp