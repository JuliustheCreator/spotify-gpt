"""
A module for fetching and processing posts from Reddit.

This module contains functions for fetching posts from Reddit using the PRAW library, processing the posts, and saving the processed data to a file.

Functions:
    setup_praw: Set up the PRAW Reddit instance.
    fetch_posts: Fetch posts from a list of subreddits.
    process_and_save_posts: Process and save the fetched posts.
"""

from utils.openai_utils import convert_data_to_knowledge
import praw
import os

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
    for subreddit, posts in posts.items():
        data_string = "\n\n".join([f"Title: {post['title']}\nURL: {post['url']}\nContent: {post['selftext']}" for post in posts])
        
        processed_data = convert_data_to_knowledge(data_string)
        
        file_name = f"data/{subreddit}_processed.txt"
        
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
    
    save_posts(posts)