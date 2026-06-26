import requests
from bs4 import BeautifulSoup
import pandas as pd

product_item = []

headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

for x in range(1, 5):
    url = f"https://www.amazon.in/s?k=instant+pot&page={x}"

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")

    material_tag = soup.find_all("div", {"data-component-type": "s-search-result"})

    for item in material_tag:

        # Title
        title = item.find("h2")
        title = title.text.strip() if title else "No title"

        # Rating
        rating_tag = item.find("span", class_="a-icon-alt")
        rating = rating_tag.text.strip() if rating_tag else "No rating"

        # Bought
        bought_tag = item.find("span", class_="a-size-base a-color-secondary")
        bought = bought_tag.text.strip() if bought_tag else "N/A"

        # Price
        price_tag = item.find("span", class_="a-price-whole")
        price = price_tag.text.strip() if price_tag else "No price"

        # Link
        link_tag = item.find("a", class_="a-link-normal s-no-outline")
        link = "https://www.amazon.in" + link_tag.get("href") if link_tag else "No link"

        # Store data
        data_dict = {
            "Title": title,
            "Rating": rating,
            "Bought": bought,
            "Price": price,
            "Full_link": link
        }

        product_item.append(data_dict)

df = pd.DataFrame(product_item)
df.to_csv("instant_pot.csv", index=False)