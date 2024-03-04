# XAI (Explainable) Music Recommendation Engine

## Project Overview
The XAI Music Recommender System is designed to provide personalized music recommendations with a focus on explainability. Unlike traditional systems, this project aims to not only match users with songs they'll love but also to provide clear, understandable reasons for each recommendation. Additionally, the system integrates cultural trends and real-time internet searches to deliver a more dynamic music discovery experience.

### Motivation
While Spotify's recommendation algorithms, such as Discover Weekly and the Playlist Enhance feature, work incredibly well, I think they fall short in two key areas:

- **Variability:** Discover Weekly can sometimes be too varied, lacking in providing a coherent explanation as to why a song is a good match for the listener.

- **Relevance and Context:** Both Discover Weekly and Enhance sometimes miss capturing the mood, tone, and genre nuances of user playlists. They also lack in explaining the cultural relevance or the sudden surge in popularity of a song, which may be important to the user.

### System Pipeline
**1. User Profile Creation**
- Input: Users describe their music preferences in natural language or provide access to their Spotify playlists.
- Process: The system employs OpenAI's GPT to parse and analyze these descriptions, creating a rich user profile that encapsulates favorite genres, artists, moods, and specific listening contexts.

**2. Real-time Integration**
- Input: Data on trending music, sourced from social media, news articles, and viral content via the Bing Search API.
- Process: The system is designed to periodically refresh its understanding of the musical landscape with this data.
  
**3. Personalized Recommendation Engine**
- Process: This core component synthesizes insights from the user's profile with real-time cultural trends, the recommendation engine will be powered through GPT.
- Output: Users receive a curated list of song recommendations that reflect their stated preferences and the latest music trends.
  
**4. Explanation Generation**
- Process: For each recommendation, the system generates a user-friendly explanation, explaining why a particular song matches the user's profile and the cultural context that might make the song especially relevant or appealing.
- Output: Each recommendation is accompanied by a detailed explanation, enhancing transparency and user trust in the system.
