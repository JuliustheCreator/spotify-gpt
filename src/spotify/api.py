import requests


#################
## Spotify API ##
#################


def get_spotify_access_token(session):
    return session.get('access_token')

def fetch_user_top_tracks(access_token, time_range = 'short_term', limit = 5):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'time_range': time_range,
        'limit': limit
    }
    url = 'https://api.spotify.com/v1/me/top/tracks'
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        top_tracks_data = response.json()
        top_tracks = []
        for item in top_tracks_data['items']:
            track_name = item['name']
            artists = ', '.join(artist['name'] for artist in item['artists'])
            top_tracks.append({'name': track_name, 'artist': artists})
        return top_tracks
    else:
        print(f"Failed to fetch top tracks: {response.status_code}")
        return []
    
def fetch_top_artists(access_token, time_range = 'short_term', limit = 5):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'time_range': time_range,
        'limit': limit
    }
    url = 'https://api.spotify.com/v1/me/top/artists'
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        top_artists_data = response.json()
        top_artists = []
        for item in top_artists_data['items']:
            artist_name = item['name']
            top_artists.append({'name': artist_name})
        return top_artists
    else:
        print(f"Failed to fetch top artists: {response.status_code}")
        return []

def fetch_track_recommendations(access_token, seed_tracks, limit=5):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    params = {
        'seed_tracks': ','.join(seed_tracks),
        'limit': limit
    }
    url = 'https://api.spotify.com/v1/recommendations'
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        recommendations_data = response.json()
        recommendations = []
        for item in recommendations_data['tracks']:
            track_name = item['name']
            artists = ', '.join(artist['name'] for artist in item['artists'])
            recommendations.append({'name': track_name, 'artist': artists})
        return recommendations
    else:
        print(f"Failed to fetch recommendations: {response.status_code}")
        return []