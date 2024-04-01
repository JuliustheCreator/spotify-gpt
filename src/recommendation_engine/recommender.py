"""
A module for generating personalized music recommendations.

This module contains functions for fetching the user's top tracks from Spotify, 
generating music recommendations based on those tracks, and fetching explanations for the recommendations.

Functions:
    get_personalized_recommendations: Fetch the user's top tracks, generate recommendations, and fetch explanations.
"""

from spotify.api import fetch_user_top_tracks  
from utils.openai_utils import generate_music_recommendations, explain_music_recommendations  
from flask import session


###########################
## Recommendation Engine ##
###########################


def get_personalized_recommendations():
    """
    Fetches the user's top tracks from Spotify, generates recommendations based on those tracks,
    and then fetches explanations for those recommendations.

    Returns:
        
            recommendations (list): A list of recommended songs.
            explanations (list): A list of explanations for the recommendations.
    """

    if not session.get('access_token'):
        return None, "Access token is not available. Please log in."

    access_token = session['access_token']
    top_tracks = fetch_user_top_tracks(access_token)

    if not top_tracks:
        return None, "Failed to fetch top tracks from Spotify."

    songs = [f"{track['name']} by {track['artist']}" for track in top_tracks]

    recommendations, explanations = generate_music_recommendations(songs)

    if not recommendations:
        return None, "Failed to generate recommendations."

    thread_id = recommendations[0]['thread_id']
    explanations = explain_music_recommendations(songs, recommendations, explanations, thread_id)

    return recommendations, explanations