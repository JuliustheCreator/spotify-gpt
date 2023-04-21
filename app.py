import os
from dotenv import load_dotenv
import openai
import streamlit as st
import time

# Load environment variables from the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

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

# Frontend
st.title("Spotify Music Recommendation")
st.write("Music recommendation system built with Generative Pre-trained Transformer")

# Backend
songs = []
song_list_placeholder = st.empty()

# Adding User's Songs to List
user_input = st.text_input("Input Song and Artist:")

add_song_button = st.button("Add Song")
submit_button = st.button("Submit Songs")

if add_song_button and user_input:
    songs.append(user_input)
    song_list_placeholder.write(f"Current song list: {', '.join(songs)}")
    user_input = ""  # Clear the input box

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
