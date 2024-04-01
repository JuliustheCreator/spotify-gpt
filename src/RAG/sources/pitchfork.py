import requests
from bs4 import BeautifulSoup

#######################
## Pitchfork Scraper ##
#######################

def scrape_pitchfork_reviews():
    base_url = 'https://pitchfork.com/reviews/albums/'
    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Navigate through the HTML structure as you described
        reviews_page_contents = soup.find('div', class_='reviews-page__contents')
        review_collection_fragments = reviews_page_contents.find_all('div', class_='review-collection-fragment')
        for fragment in review_collection_fragments:
            reviews = fragment.find_all('div', class_='review')
            for review in reviews:
                review_link = review.find('a')['href']
                print(f'Review Link: https://pitchfork.com{review_link}')
    else:
        print("Failed to retrieve data")
