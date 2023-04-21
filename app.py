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
st.title("Music Recommendation App")
st.write("Music Recommendation System Built on Generative Pre-trained Transformer (Chat GPT) by Julius")

st.write("Name 5 of your favorite songs (of the same genre for best results)")

# Backend

user_input1 = st.text_input("1: ")
user_input2 = st.text_input("2: ")
user_input3 = st.text_input("3: ")
user_input4 = st.text_input("4: ")
user_input5 = st.text_input("5: ")

songs = [user_input1, user_input2, user_input3, user_input4, user_input5]

if user_input1 and user_input2 and user_input3 and user_input4 and user_input5:
    response_text = get_response(f'Name 10 more obscure artists and a recommended song of theirs if I enjoy listening to: {songs} ')
    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    st.write(response_text)

