from bs4 import BeautifulSoup
import pandas as pd
import requests

product_info = []


website = "https://news.ycombinator.com/news" 
r = requests.get(website)
soup = BeautifulSoup(r.content,"html.parser")


articles_info = soup.find_all("span",class_ = "titleline")
upvotes_info = soup.find_all("span",class_ = "subline")




for i in range(len(articles_info)):
    item = articles_info[i]
    articles_name = item.find("a").getText()
    article_link= item.find("a")["href"]
    #points
    sub = upvotes_info[i]
    try:
        upvotes = int(sub.find("span",class_ = "score").getText().split()[0]) 
    except:
        upvotes = 0
    #author
    try:
        author = sub.find("a",class_ = "hnuser").getText()
    except:
        author = "None"
    #Time
    try:
        time = sub.find("span",class_ = "age").getText()
    except:
        time = "None"
    #comment
    try:
        comment = sub.find_all("a")[-1].getText()
    except:
        comment = "0 comment"




    articles_data = {
        "name": articles_name,
        "link" : article_link,
        "upvotes":upvotes,
        "author":author,
        "time":time,
        "comment":comment
    }
    product_info.append(articles_data)

df = pd.DataFrame(product_info)
df.to_csv("articles_list.csv",index = False)