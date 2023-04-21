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
st.subheader("Music recommendation system built with Generative Pre-trained Transformer")

st.write("Name as many of your favorite songs as you'd like! (of the same genre for best results)")

# Backend

button = st.button('Finish')
songs = []
TEXT = f'Name 10 obscure artists I am sure to enjoy, as well as a recommended song of theirs if I enjoy listening to: {songs}'

# Adding User's Songs to List
while (not button) and len(songs):
    user_input = st.text_input("Input Song and Artist: ")
    songs.append(user_input)

# Fetching Response
response_text = get_response(TEXT)

# Progress Bar
latest_iteration = st.empty()
bar = st.progress(0)
for i in range(100):
    bar.progress(i + 1)
    time.sleep(0.1)

# Print Response
st.write(response_text)

