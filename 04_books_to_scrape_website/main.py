import requests
import pandas as pd
from bs4 import BeautifulSoup

books_info = []

for x in range(1,51):
    website = (f"https://books.toscrape.com/catalogue/page-{x}.html")

    r = requests.get(website)
    soup = BeautifulSoup(r.content,"html.parser")
    book = soup.find_all("li",class_ = "col-xs-6 col-sm-4 col-md-3 col-lg-3")


    for item in book:
        name_tag = item.find("h3").find("a")
        book_name = name_tag.text.strip()
        book_link = name_tag["href"]
        book_price = item.find("p",class_ = "price_color").text.strip()

        all_products = {
            "Name" : book_name,
            "Link":  book_link,
            "Price" : book_price
        }

        books_info.append(all_products)


df = pd.DataFrame(books_info)    
df.to_csv("04_Books_info.csv",index = False)