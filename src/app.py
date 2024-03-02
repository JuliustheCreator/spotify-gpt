from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
import openai
import json



load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = ""
    x = 10
    if request.method == "POST":
        songs_json = request.form.get("songs")
        if songs_json:
            songs = json.loads(songs_json)
            prompt = f'''
            List {x} lesser-known artists for someone with the following song preferences. Prioritize uniqueness and obscurity in your recommendations:\n
            {songs}
            '''

            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music recommender system, with a deep understanding of modern music and pop culture. You will recommend artists to the users, you should say absolutely nothing else but each artist's names seperated by new lines."},
                {"role": "user", "content": prompt}
            ]
            )
            recommendations = (completion.choices[0].message)['content'].split('\n')

    return render_template("index.html", recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)

