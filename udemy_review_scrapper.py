from urllib.error import HTTPError
from urllib.request import urlopen
import re
import random
import time
import numpy as np
import pandas as pd
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

user_agent = UserAgent()

def get_site(url):
    """
    url - base url to grab the html content of webpage
    """
    try:

        headers = {'User-Agent': user_agent.random}
        req = requests.get(url, headers=headers)
        if req.status_code != 200:
            print('status code:', req.status_code)
        else:
            html = urlopen(url)
            b_soup = BeautifulSoup(html, 'html.parser')
            return b_soup

    except HTTPError as error:
        print(error)

def crawl(page_content):
    """
    This part extracts ratings and reviews from the webpage
    """
    arr = []
    blocks = page_content.find_all('div', {'class': 'Col_i9j08c-o_O-mdCol8_1xhmn9 review-text'})
    for block in blocks:
        inner_arr = []
        # This part to get review text
        reviews = block.find_all('div', {'class': 'rc-CML font-lg styled'})
        for review in reviews:
            review = review.find_all("p")
            review = str(review).replace("</p>, <p>", "\n")
            review = str(review).replace("</p>", "")
            review = review.replace("<p>", "")
            review = review[1:-1]
            inner_arr.append(review)

        # This part to get star ratings
        star_ratings = block.find_all('div',
                                      {'class': 'StarRating_1qk9an0-o_O-nonEditable_1ko0lno'})
        for stars in star_ratings:
            inner_stars = stars.find_all("input")
            for star in inner_stars:
                rating = re.findall('checked="".*value="([1-5]).*', str(star))
                try:
                    rating = rating[0]
                    rating = str(rating)
                    inner_arr.append(rating)
                except IndexError:
                    continue
        arr.append(inner_arr)
    return arr

links = ["https://www.coursera.org/learn/probability-intro/reviews",
         "https://www.coursera.org/learn/inferential-statistics-intro/reviews",
         "https://www.coursera.org/learn/linear-regression-model/reviews",
         "https://www.coursera.org/learn/bayesian/reviews",
         "https://www.coursera.org/learn/statistics-project/reviews",
         "https://www.coursera.org/learn/understanding-visualization-data/reviews",
         "https://www.coursera.org/learn/inferential-statistical-analysis-python/reviews",
         "https://www.coursera.org/learn/fitting-statistical-models-data-python/reviews",
         "https://www.coursera.org/learn/linear-algebra-machine-learning/reviews",
         "https://www.coursera.org/learn/multivariate-calculus-machine-learning/reviews",
         "https://www.coursera.org/learn/pca-machine-learning",
         "https://www.coursera.org/learn/ml-foundations/reviews",
         "https://www.coursera.org/learn/ml-regression/reviews",
         "https://www.coursera.org/learn/ml-classification",
         "https://www.coursera.org/learn/ml-clustering-and-retrieval",
         "https://www.coursera.org/learn/probabilistic-graphical-models/reviews",
         "https://www.coursera.org/learn/probabilistic-graphical-models-2-inference/reviews",
         "https://www.coursera.org/learn/probabilistic-graphical-models-3-learning/reviews",
         ]

webpage = "https://www.coursera.org/learn/neural-networks-deep-learning/reviews"
time.sleep(random.randint(2, 10))
for i in range(1, 2):
    webpage = webpage + '?page=' + str(i)
    page_content = get_site(webpage)
    if page_content is not None:
        array = crawl(page_content)
        df = np.row_stack((array))
        my_df = pd.DataFrame(df)
        my_df.to_csv('answers.csv', mode='a', index=False, header=False)
#        df = pd.DataFrame(np.concatenate(array))
#    df.to_csv('reviews.csv', mode='a', index=False, header=False)
