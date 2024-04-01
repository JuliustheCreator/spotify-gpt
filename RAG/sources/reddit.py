import praw
import os
import json

######################
## Reddit Functions ##
######################

def setup_praw():
    return praw.Reddit(client_id=os.getenv('REDDIT_CLIENT_ID'),
                       client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                       user_agent='XAI-MRS')

def fetch_posts(subreddit_names, reddit_instance, posts_per_sub = 50):
    post_container = {}
    for subreddit_name in subreddit_names:
        subreddit = reddit_instance.subreddit(subreddit_name)
        posts = []
        for post in subreddit.hot(limit = posts_per_sub):
            post_data = {
                "title": post.title,
                "url": post.url,
                "subreddit": subreddit_name,
                "selftext": post.selftext if post.selftext else "No content"
            }
            posts.append(post_data)
        post_container[subreddit_name] = posts
    return post_container

def save_posts(posts):
    try:
        with open('posts.json', 'w', encoding = 'utf-8') as f:
            json.dump(posts, f, ensure_ascii = False, indent = 4)
    except Exception as e:
        print(f"An error occurred while saving posts: {e}")

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
    save_posts(posts)


