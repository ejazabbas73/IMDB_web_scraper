import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
from string import digits

def Top250Movies(url):
    titles = []
    ratings = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    with requests.Session() as session:
        req = session.get(url, headers=headers)
        req.raise_for_status() 
        content = BeautifulSoup(req.content, 'html.parser')

    data = content.find_all('li', {'class': 'ipc-metadata-list-summary-item'})
    for i in data:
        ti  = i.find('h3', attrs={'class': 'ipc-title__text'})
        ra  = i.find('span', attrs={'class': 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'})
        titles.append(ti.text.strip(f"{digits}."))
        ratings.append(ra.text.strip())

    return titles, ratings

start_time = time.time()
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
titles, ratings = Top250Movies(url)

df = {'Titles': titles, 'Ratings': ratings}
finaldf = pd.DataFrame(df)
finaldf.to_excel('Top 250 movies data.xlsx', index=False)

end_time = time.time()

print(f"Total Data is Scraped in {end_time - start_time:.1f} Seconds")
print("---------------------------------------------------------------------------------------------------")
