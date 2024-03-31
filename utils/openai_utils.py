import openai
import os
import time
import json


##################
## OpenAI Utils ##
##################


openai.api_key = os.environ.get("OPENAI_API_KEY")
assistant_id = os.environ.get("OPENAI_ASSISTANT_ID")

client = openai.OpenAI()

def generate_music_recommendations(songs: list):
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
            assistant_id=assistant_id,
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
            assistant_id=assistant_id,
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

        explanations = [item['reason'] for item in response['recommendations']]

        return explanations
    
    except Exception as e:
        print(f"Error generating explanations: {e}")
        return ["Error generating explanations."]