from utils.openai_utils import convert_data_to_knowledge
from RAG.sources.reddit import setup_praw, fetch_posts
from openai import OpenAI


################
## RAG Script ##
################

client = OpenAI()

def save_reddit_posts(posts):
    for subreddit, posts in posts.items():
        data_string = "\n\n".join([f"Title: {post['title']}\nURL: {post['url']}\nContent: {post['selftext']}" for post in posts])
        
        processed_data = convert_data_to_knowledge(data_string)
        
        file_name = f"data/REDDIT-{subreddit}.txt"
        
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(processed_data)
        except Exception as e:
            print(f"An error occurred while saving processed posts for {subreddit}: {e}")

if __name__ == "__main__":
    reddit = setup_praw()
    subreddits = [
        'jazz', 
        'hiphopheads', 
        'listentothis', 
        'indieheads', 
        'letstalkmusic', 
        'popheads', 
        'rnb', 
        'postrock', 
        'electronicmusic'
    ]

    posts = fetch_posts(subreddits, reddit)

    save_reddit_posts(posts)