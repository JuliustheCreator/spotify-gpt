import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config.settings import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

def authenticate_spotify():
    """Authenticate with Spotify using Spotipy."""
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_artist(sp, artist_id):
    """Fetch artist data from Spotify."""
    return sp.artist(artist_id)

def get_track(sp, track_id):
    """Fetch track data from Spotify."""
    return sp.track(track_id)

def get_album(sp, album_id):
    """Fetch album data from Spotify."""
    return sp.album(album_id)

def get_tracks_from_album(sp, album_id):
    """Fetch all tracks from an album."""
    album_tracks = sp.album_tracks(album_id)
    return album_tracks['items']