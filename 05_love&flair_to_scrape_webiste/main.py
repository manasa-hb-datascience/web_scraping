import requests
from bs4 import BeautifulSoup
import pandas as pd 


baseurl = "https://loveandflair.com/"

header = {
    'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
}
productlinks = []
productdata = []
for x in range (1,11):
    r = requests.get(f"https://loveandflair.com/collections/activewear-1?page={x}")
    soup =  BeautifulSoup(r.content,"html.parser")

    productlist = soup.find_all("div",class_ = "card-wrapper js-color-swatches-wrapper")

    for item in productlist:
        for link in item.find_all("a",class_ = "link link--overlay card-wrapper__link--overlay card-product__link js-color-swatches-link"):
            productlinks.append(baseurl + link['href'])

productlinks = list(set(productlinks))

for link in productlinks:
    r = requests.get(link,headers = header)

    soup = BeautifulSoup(r.content,"html.parser")

    name = soup.find("h4",class_ = "product__title")
    name_tag = name.text.strip() if name else  "No_Name"


    price = soup.find("span",class_ = "money")
    price_tag = price.text.strip() if price else "no_price"

    stock = soup.find("span",class_ = "advantage__title")
    stock_tag = stock.text.strip() if stock else "no_stock"

    color = soup.find_all("label",class_ = "color-swatch")
    color_list = [c.get("title") for c in color if c.get("title")]
    color_tag = ",".join(color_list)if color_list else "no_colr"         

    size = soup.find_all("input",{"type":"radio"})
    size_list = [s.get("value") for s in size if s.get("value")]
    sizelist = list(set(size_list)) 
    size_tag = ",".join(size_list)if size_list else "No_size"
           

    material_tag = "no_material"
    label = soup.find("span")
    for l in label:
        labels = l.text.strip()
        if labels and labels.isupper() and len(labels) < 30:
            if "SOFTCLOUD" and "CLOUD" in labels:
                material_tag = labels
                break
    

    data = {
        "name": name_tag,
        "price": price_tag,
        "stock" : stock_tag,
        "color": color_tag,
        "size": size_tag,
        "material": material_tag,
        "link":link
    }

    productdata.append(data)

df = pd.DataFrame(productdata)
df.to_csv("loveandflair.csv",index=False)