# XAI Music Recommender System

## Motivation
This project is an attempt at refining music recommendation systems (MRSs) by leveraging the capabilities of Large Language Models (LLMs), specifically OpenAI's models, and Explainable Artificial Intelligence (XAI). Traditional systems often leave out why certain recommendations are made, leaving users puzzled about their music queues. The project's goal aim is to not only generate more relevant, personalized recommendations but also provide clear, detailed explanations for each, merging the interpretability of XAI with the depth of understanding provided by LLMs. 

Furthermore, despite the success of Spotify's MRSs like Discover Weekly and the Playlist Enhance feature, there remains a gap in variability and contextual relevance. This system addresses these shortcomings by enhancing variability through explainable, data-driven insights and improving relevance by incorporating real-time cultural and internet trends.


## System Design
### Data Collection and User Profile Creation
**Spotify Playlists:** Songs from users' Spotify playlists are categorized using metadata such as genre, mood, and tempo. This categorization feeds into a detailed user profile that reflects their musical tastes and preferences.

**Social Media Integration (Reddit):** To capture real-time trends and broader cultural contexts, we'll scrape Reddit discussions related to music. This is achieved using the Retrieval-Augmented Generation (RAG) model, which combines the power of a retriever to fetch relevant data and a generator to synthesize this information.
### Recommendation Engine
**OpenAI's LLMs for Personalized Recommendations:** Utilizing models like GPT-4 and GPT-3 for parsing user inputs and generating music recommendations. These models are adept at understanding complex user descriptions and matching them with suitable music choices by analyzing the user profile and current trends.

**RAG for Trend Integration:** The RAG model plays a crucial role in integrating real-time data from Reddit, ensuring that recommendations are not only personalized but also contextually relevant and culturally aware.
### Explainable AI (XAI) Approaches
**Intrinsic Explainability with Chain of Thought (CoT) Prompting:** Leveraging CoT prompting in LLMs to inherently provide explanations about why particular songs or artists are recommended, making the process transparent at the model level.

**Ex Post Facto Explainability for Content-based Recommendations:** Even though LLM-based recommendations naturally lend themselves to explainability through CoT, the content-based aspect of our system — focusing on song features like mood and tempo — requires additional clarity. Here, we'll use a post-hoc explanation approach, where an LLM synthesizes all available data (user preferences, song features, and cultural trends) to articulate clear, logical reasons behind each recommendation.

**Two-Modal Explanation Framework:** Combining the comprehensive, language-based explanations from LLMs with data visualizations that highlight similarities in song and artist features. This dual approach caters to diverse user preferences for understanding their music recommendations, offering both a narrative and visual understanding of the recommendation process.

### Simple Technical Stack Overview

#### Backend
- **Framework**: Flask
- **Task Queue**: Celery with Redis for asynchronous task management
- **Database**: PostgreSQL

#### AI and Machine Learning
- **LLMs and Models**: OpenAI's GPT-4 for user input analysis and recommendation generation. RAG for integrating real-time trends from Reddit.
- **XAI Methods**: Chain of Thought (CoT) prompting for explainable recommendations. Custom scripts for ex post facto explanations and data visualizations.

#### Frontend
- **Framework**: Vue.js
