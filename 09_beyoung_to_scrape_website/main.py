import requests
import pandas as pd
from bs4 import BeautifulSoup

product_info = []
product_links = []

baseurl = "https://www.beyoung.in"
headers = {
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
    }
for x in range(0,200,12):
    url = (f"https://www.beyoung.in/mens-new-arrival?limit=12&offset={x}")
    r = requests.get(url)

    soup = BeautifulSoup(r.content,"html.parser")

    productlist = soup.find_all("div",class_ = "products")

    for item in productlist:
        for link in  item.find_all("a",href = True): # gives main link off all products and remove dublicates from links and make list
           product_links.append(baseurl + link['href'])

product_links = list(dict.fromkeys(product_links))


# testlink = "https://www.beyoung.in/mauve-linen-striped-shirt"
for link in product_links:
    r = requests.get(link,headers = headers)

    soup = BeautifulSoup(r.content,"html.parser")
    # product name
    product_name = soup.find("h1").text.strip()
    #discounted price
    discounted_price = soup.find("span",class_ = "realprice").text.strip()
    #regular price
    regular_price = soup.find('span',class_ = "cuttinprice").text.strip()
    #discount
    discount = soup.find("div",class_ = "slanted-box").text.strip()
    product_data = {
        "Product_name":product_name,
        "Discounted_price":discounted_price,
        "Regula_price":regular_price,
        "Discount":discount,
        "Full_link":link
    }

    product_info.append(product_data)


df = pd.DataFrame(product_info)
df.to_csv("beyoung.csv",index = False)
print("successfully")