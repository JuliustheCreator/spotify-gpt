import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Spotify API credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('STREAMLIT_APP_URL')+ "/auth"

scope = 'user-top-read playlist-modify-public'

# ChatGPT API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Authenticate with Spotify
auth_manager = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope,
                            show_dialog=True)

sp = spotipy.Spotify(auth_manager=auth_manager)

# Function to use ChatGPT API
def request_gpt(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.2,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    song_list = response.choices[0].text.strip().split("\n")
    return song_list

# Streamlit frontend
st.title("Spotify Music Recommendation")
st.write("Music recommendation system built with Generative Pre-trained Transformer")

# Check if user is authenticated
if auth_manager.get_cached_token():
    # Get user's top artists and songs 
    top_artists = sp.current_user_top_artists(limit=5)
    top_tracks = sp.current_user_top_tracks(limit=5)

    # Combine artists and songs into a string
    user_music = ', '.join([artist['name'] for artist in top_artists['items']] + [track['name'] for track in top_tracks['items']])

    # Generate a prompt for ChatGPT
    prompt = f"Create a playlist of 20 songs based on the user's favorite artists and songs: {user_music}"

    # Get recommendations from ChatGPT
    recommended_songs = request_gpt(prompt)

    if recommended_songs:
        st.write("Fetching recommendations...")
        bar = st.progress(0)
        for i in range(100):
            bar.progress(i + 1)
            time.sleep(0.01)

        # Get title from ChatGPT
        title = request_gpt(f'Give me a playlist title for {recommended_songs}')

        # Create a new playlist
        user_id = sp.current_user()['id']
        playlist_name = title
        playlist_description = "A playlist automatically created using the Spotify API and ChatGPT."

        playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description=playlist_description)
        playlist_id = playlist['id']

        # Add recommended songs to the playlist
        track_uris = [song['uri'] for song in recommended_songs]
        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)

        # Show success message
        st.write(f"Successfully created a new playlist named '{playlist_name}' based on your favorite artists and songs!")
    else:
        st.write("Couldn't generate any recommendations. Please try again.")
else:
    # Redirect the user to the Spotify authorization URL
    auth_button = st.button("Authenticate with Spotify")
    if auth_button:
        # Redirect the user to the Spotify authorization URL
        auth_url = auth_manager.get_authorize_url()
        st.markdown(f'<a href="{auth_url}" target="_blank">Click here to authenticate with Spotify</a>', unsafe_allow_html=True)

# Handle authentication callback
path = st.experimental_get_query_params().get("path")
if path == ["auth"]:
    code = st.experimental_get_query_params().get("code")
    if code:
        token_info = auth_manager.get_access_token(code[0], check_cache=False)
        auth_manager._save_token_info(token_info)
        st.experimental_set_query_params(path="", code="")
        st.experimental_rerun()
