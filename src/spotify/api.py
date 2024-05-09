import requests


#################
## Spotify API ##
#################


def get_spotify_access_token(session):
    return session.get('access_token')

def fetch_user_top_tracks(access_token, time_range='short_term', limit=20):
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