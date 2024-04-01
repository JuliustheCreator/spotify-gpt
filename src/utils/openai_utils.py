"""
Utility functions for interacting with the OpenAI API.

This module provides functions for generating music recommendations and explanations using the OpenAI API.

Functions:
    generate_music_recommendations: Generate music recommendations based on a list of songs.
    explain_music_recommendations: Explain music recommendations based on a list of songs and recommendations.
    split_text_into_chunks: Split text into chunks of a specified maximum number of words.
    process_chunk: Process a chunk of text using the OpenAI API.
    convert_data_to_knowledge: Convert data to knowledge using the OpenAI API.
"""

from dotenv import load_dotenv
import openai
import os
import time
import json

##################
## OpenAI Utils ##
##################

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
MRS_assistant_id = os.environ.get("MRS_ASSISTANT_ID")
RAG_assistant_id = os.environ.get("RAG_ASSISTANT_ID")

client = openai.OpenAI()

def generate_music_recommendations(songs: list):
    '''
    Generate music recommendations based on a list of songs.
    
    Args:

        songs (list): A list of songs to generate recommendations from.

    Returns:

        recommendations (list): A list of recommended songs.
    '''

    try:
        thread = client.beta.threads.create()
    except Exception as e:
        print(f"Error creating thread: {e}")
        return ["Error creating thread."]

    try:
        message = client.beta.threads.messages.create(
            thread_id = thread.id,
            role = "user",
            content = f"Based on these artists: {', '.join(songs)}, recommend 7 new and unique songs I'll enjoy",
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=MRS_assistant_id,
        )

        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        response = messages.data[0].content[0].text.value
        response = json.loads(response)

        recommendations = [{'song': item['song'], 'artist': item['artist']} for item in response['recommendations']]
        explanations = [item['reason'] for item in response['recommendations']]

        return recommendations, explanations
    
    except Exception as e:
        print(f"Error generating recommendations: {e}")
        return ["Error generating recommendations."]


def explain_music_recommendations(songs: list, recommendations: list, explanations: list, thread):
    '''
    Explain music recommendations based on a list of songs and recommendations.

    Args:

            songs (list): A list of songs.
            recommendations (list): A list of recommended songs.
            explanations (list): A list of explanations for the recommendations.
            thread: The thread to use for generating explanations.

    Returns:

            explanations (list): A list of explanations for the recommendations.
    '''
    try:
        message = client.beta.threads.messages.create(
            thread_id = thread.id,
            role = "user",
            content = f'''
            Based on these songs: {', '.join(songs)}, explain why I might like these songs: {', '.join(recommendations)}. 
            You should use your updated knowledge base as well as the following information: {explanations}
            ''',
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=MRS_assistant_id,
        )

        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id,
            )
            time.sleep(0.5)
        
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        response = messages.data[0].content[0].text.value
        response = json.loads(response)

        explainations = [item['reason'] for item in response['recommendations']]

        try:
            client.beta.threads.delete(thread.id)
        except Exception as e:
            print(f"Error deleting thread: {e}")
            return "Error deleting thread."

        return explainations
    
    except Exception as e:
        print(f"Error generating explanations: {e}")
        return ["Error generating explanations."]    
    
def split_text_into_chunks(text, max_words = 1000):
    '''
    Split text into chunks of a specified maximum number of words.

    Args:

        text (str): The text to split into chunks.
        max_words (int): The maximum number of words per chunk.
    
    Returns:

        chunks (list): A list of text chunks.
    '''

    words = text.split()
    chunks = [' '.join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return chunks

def process_chunk(chunk, thread_id):
    '''
    Process a chunk of text using the OpenAI API.
    
    Args:
    
        chunk (str): The text chunk to process.
        thread_id (str): The thread ID to use for processing the chunk.
        
    Returns:
        
        result (str): The result of processing the chunk.
    '''
    
    try:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=chunk,
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=RAG_assistant_id,
        )

        while run.status == "queued" or run.status == "in_progress":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id,
            )
            time.sleep(0.5)
        
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        response = messages.data[0].content[0].text.value
        print(response)
        
        return response
    
    except Exception as e:
        print(f"Error processing chunk: {e}")
        return ""

def convert_data_to_knowledge(data):
    '''
    Convert data to knowledge using with the OpenAI API using recursive decomposition.

    Args:
    
            data (str): The data to convert to knowledge.

    Returns:
    
            combined_result (str): The combined result of processing the data.
    '''
    try:
        thread = client.beta.threads.create()
    except Exception as e:
        print(f"Error creating thread: {e}")
        return "Error creating thread."

    chunks = split_text_into_chunks(data)
    results = []

    for chunk in chunks:
        result = process_chunk(chunk, thread.id)
        results.append(result)

    try:
        client.beta.threads.delete(thread.id)
    except Exception as e:
        print(f"Error deleting thread: {e}")

    if not results: return ""

    combined_result = ' '.join(results)
    return combined_result

