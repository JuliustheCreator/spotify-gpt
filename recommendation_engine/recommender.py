from spotify.api import fetch_user_top_tracks  # This function needs to be implemented in spotify/api.py
from utils.openai_utils import generate_music_recommendations  # Assumes this is already implemented
from flask import session


###########################
## Recommendation Engine ##
###########################


def get_personalized_recommendations():
    if not session.get('access_token'):
        return "Access token is not available. Please log in.", False

    access_token = session['access_token']
    top_tracks = fetch_user_top_tracks(access_token)

    if not top_tracks:
        return "Failed to fetch top tracks from Spotify.", False

    songs = [f"{track['name']} by {track['artist']}" for track in top_tracks]

    recommendations, explanations = generate_music_recommendations(songs)

    if not recommendations:
        return "Failed to generate recommendations.", False

    recommendations = "\n".join(recommendations)
    explanations = "\n".join(explanations)

    return recommendations, explanations

