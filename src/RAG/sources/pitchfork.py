"""
A module for fetching and processing reviews from Pitchfork.

This module contains functions for fetching review links from the Pitchfork website, 
scraping the details of each review, and saving the review details to a JSON file.

Functions:
    get_review_links: Get review links from the Pitchfork website.
    scrape_review_details: Scrape the details of a review from a review URL.
"""

import requests
import json
from bs4 import BeautifulSoup

#######################
## Pitchfork Scraper ##
#######################

def get_review_links(base_url, start_page=1, end_page=50):
    all_review_links = []
    
    for page_num in range(start_page, end_page + 1):
        url = f"{base_url}?page={page_num}"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            review_fragments = soup.find_all('div', class_='review-collection-fragment')
            
            for fragment in review_fragments:
                reviews = fragment.find_all('div', class_='review')
                for review in reviews:
                    link_tag = review.find('a', class_='review__link')
                    if link_tag and 'href' in link_tag.attrs:
                        link = link_tag['href']
                        full_link = f"https://pitchfork.com{link}"
                        all_review_links.append(full_link)
            print(f"Page {page_num}: Found {len(all_review_links)} links so far.")
        else:
            print(f"Failed to retrieve page {page_num}")
            break

    return all_review_links

def scrape_review_details(review_url: str):
    response = requests.get(review_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    rating = soup.find('p', class_='Rating-iATjmx').text
    try:
        title = soup.find('h1', {"data-testid": "ContentHeaderHed"}).text
    except:
        return None
    artist = soup.find('div', class_='SplitScreenContentHeaderArtist-ftloCc').text
    genre = soup.find('p', class_='InfoSliceValue-tfmqg').text
    description = soup.find('div', class_='SplitScreenContentHeaderDekDown-csTFQR').text
    
    review_details = {
        'URL': review_url,
        'Rating': rating,
        'Title': title,
        'Artist': artist,
        'Genre': genre,
        'Description': description
    }
    
    return review_details

def save_to_json(links, filename="data/pitchfork.json"):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(links, file, ensure_ascii=False, indent=4)
    print(f"Saved {len(links)} links to {filename}")

if __name__ == "__main__":
    base_url = 'https://pitchfork.com/reviews/albums/'
    review_links = get_review_links(base_url, 1, 25)
    
    all_review_details = []
    for link in review_links:
        details = scrape_review_details(link)
        all_review_details.append(details)

    save_to_json(all_review_details)