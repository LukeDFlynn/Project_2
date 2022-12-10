import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from gui2 import *

def scrapeMovie(status):

    headers = {"Accept-Language": "en-US,en; q=0.5"}

    movie_name = []
    year = []
    time = []
    rating = []
    metascore = []
    votes = []
    gross = []
    count = 0

    pages = np.arange(1, 1000, 100)

    for page in pages:
        page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(page)+"&ref_=adv_nxt")
        soup = BeautifulSoup(page.text, 'html.parser')
        movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})
        sleep(randint(2, 8))
        if count < 9:
            print(f"Page {count+1} of 10 complete.")
        else:
            print("Movies exported successfully!")
        for store in movie_data:
            name = store.h3.a.text
            movie_name.append(name)

            year_of_release = store.h3.find('span', class_="lister-item-year text-muted unbold").text
            year.append(year_of_release)

            runtime = store.p.find("span", class_='runtime').text
            time.append(runtime)

            rate = store.find('div', class_='inline-block ratings-imdb-rating').text
            rating.append(rate)

            meta = store.find('span', class_='metascore').text if store.find('span', class_='metascore') else "****"
            metascore.append(meta)

            value = store.find_all('span', attrs={'name': 'nv'})

            vote = value[0].text
            votes.append(vote)

            grosses = value[1].text if len(value)>1 else '%^%^%^'
            gross.append(grosses)
        count = count + 1

    movie_list = pd.DataFrame({"Movie Name": movie_name, " Year of Release": year, " Watch Time": time, " Movie Rating": rating, " Metascore of Movie": metascore, " Votes": votes, "  Gross": gross})
    if status == "excel":
        movie_list.to_excel("List of top 1000 Movies by IMDb.xlsx")
    else:
        movie_list.to_csv("List of top 1000 Movies by IMDb.csv")

def scrapeBook(status):

    books = []
    num = 0
    for i in range(1, 51):
        url = f"https://books.toscrape.com/catalogue/page-{i}.html"

        print(f"page {i} processing...")

        response = requests.get(url)
        response = response.content

        soup = BeautifulSoup(response, 'html.parser')
        ol = soup.find('ol')
        articles = ol.find_all('article', class_='product_pod')

        for article in articles:
            image = article.find('img')
            title = image.attrs['alt']
            star = article.find('p')
            star = star['class'][1]
            price = article.find('p', class_='price_color').text
            price = float(price[1:])
            books.append([title, price, star])

    books = pd.DataFrame(books, columns=['Title', 'Price', 'Star Rating'])
    if status == 'csv':
        books.to_excel("Books.xlsx")
    else:
        books.to_csv("Books.xlsx")


def main():
    app = QApplication([])
    window = Controller()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
