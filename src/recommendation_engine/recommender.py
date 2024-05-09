"""
A module for generating personalized music recommendations.

This module contains functions for fetching the user's top tracks from Spotify, 
generating music recommendations based on those tracks, and fetching explanations for the recommendations.

Functions:
    get_recommendations: Fetch the user's top tracks, generate recommendations, and fetch explanations.
"""

from spotify.api import fetch_user_top_tracks
from utils.langchain_utils import RecommendationLLM, ExplanationLLM  
from flask import session


###########################
## Recommendation Engine ##
###########################


def get_recommendations():
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

    songs = str([f"{track['name']} by {track['artist']}" for track in top_tracks])

    try:
        recommendationLLM = RecommendationLLM()
        explanationLLM = ExplanationLLM()

        recommendations = recommendationLLM(songs)
        print(recommendations)

        recommendations = explanationLLM(recommendations)
        print(recommendations)

        # recommendations = explanationLLM(
        #     recommendationLLM(songs)
        #     )
    
    except Exception as e:
        return None, f"Error processing recommendations: {str(e)}"

    return recommendations