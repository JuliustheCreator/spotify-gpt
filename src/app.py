from flask import Flask, request, render_template, session
from flask_session import Session  # You may need to install Flask-Session
import os
from dotenv import load_dotenv
import openai



load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
app.secret_key = 'ANGP0618'  
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if 'songs' not in session:
        session['songs'] = []
    
    recommendations = ""
    if request.method == "POST":
        song_action = request.form.get("action")
        song = request.form.get("song")
        
        if song_action == "Add Song" and song:
            session['songs'].append(song)
            session.modified = True 
        elif song_action == "Submit Songs" and session['songs']:
            prompt = f'Name 10 obscure artists I am sure to enjoy, as well as a recommended song of theirs if I enjoy listening to: {session["songs"]}'
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            recommendations = response.choices[0].text.strip()
            session['songs'].clear() 
            
    return render_template("index.html", songs=session.get('songs', []), recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
