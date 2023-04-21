import os
from dotenv import load_dotenv
import openai
import streamlit as st
import time
from spotipy.oauth2 import SpotifyOAuth
import urllib.parse

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Setting up Spotify Auth
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'https://your_streamlit_app_url/callback'
scope = 'playlist-modify-public'

auth_manager = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope,
                            show_dialog=True)

# Check if an authorization code is in the URL query parameters
query_params = st.experimental_get_query_params()
auth_code = query_params.get('code', [None])[0]

if auth_code:
    # Get access token using the authorization code
    auth_manager.get_access_token(auth_code)
    
    if auth_manager.get_cached_token():
        # Proceed with the authenticated actions (e.g., creating playlists)
        st.write("You are now authenticated.")
    else:
        st.warning("Failed to authenticate.")
else:
    # Redirect the user to the Spotify authorization URL
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"[Click here to authenticate with Spotify.]({auth_url})")
    
# Send a message request and get the response
def get_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

# C
st.title("Spotify Music Recommendation")
st.write("Music recommendation system built with Generative Pre-trained Transformer")

# Backend
songs = []
song_list_placeholder = st.empty()

# Adding User's Songs to List
user_input = st.text_input('', placeholder = "Input Song and Artist")

add_song_button = st.button("Add Song.")
st.empty()
submit_button = st.button("Submit Songs.")

if add_song_button and user_input:
    songs.append(user_input)
    song_list_placeholder.write(f"Songs & Artist: {', '.join(songs)}")
    user_input = "" 

# Fetching Response
if submit_button and len(songs) > 0:
    TEXT = f'Name 10 obscure artists I am sure to enjoy, as well as a recommended song of theirs if I enjoy listening to: {songs}'
    response_text = get_response(TEXT)

    # Progress Bar
    st.write("Fetching recommendations...")
    bar = st.progress(0)
    for i in range(100):
        bar.progress(i + 1)
        time.sleep(0.01)

    # Print Response
    st.write(response_text)
elif submit_button:
    st.warning("Please add at least one song before submitting.")
