import requests
import pandas as pd
from bs4 import BeautifulSoup

quotes_data = []

for x in range(1,11):
    website = (f"https://quotes.toscrape.com/page/{x}/")
    r = requests.get(website)
    soup =BeautifulSoup(r.content,"html.parser")
    quotes_detail = soup.find_all("div",class_ = "quote")

    for item in quotes_detail:
        quotes = item.find("span",class_ = "text").text.strip()
        author = item.find("small",class_ = "author").text.strip()
        author_link = item.find("a")["href"]
        tags = [tag.text for tag in  item.find("div",class_ = "tags").find_all("a")]

        data = {
            "Quotes": quotes,
            "Author":author,
            "Author_link":author_link,
            "Tags" :tags
        }

        quotes_data.append(data)


df  = pd.DataFrame(quotes_data)
df.to_csv("quotes.csv",index = False)