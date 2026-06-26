import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.allrecipes.com/"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
}

productitem = []
productlinks = []

for x in range(1,6):
    url = (f"https://www.allrecipes.com/recipes/1509/holidays-and-events/cinco-de-mayo/?page={x}")

    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content,"html.parser")
    recipes_info = soup.find('div',class_ = "loc fixedContent")

    links = recipes_info.find_all('a',href = True)

    for link in links:
        productlinks.append(link['href'])
productlinks = list(set(productlinks))
print(len(productlinks))

for link in productlinks:
# testlink = "https://www.allrecipes.com/recipe/139603/slow-cooker-carnitas/"
    r = requests.get(link,headers = headers)
    soup = BeautifulSoup(r.content,"html.parser")

    food_recipe = soup.find('h1',class_ = 'article-heading text-headline-400')
    food_recipes = food_recipe.text.strip() if food_recipe else 'No'

    food_rating = soup.find('div',id = "mm-recipes-review-bar__rating_1-0")
    food_ratings  = food_rating.text.strip() if food_rating else "No"

    food_review = soup.find('div',class_ = "comp mm-recipes-review-bar__comment-count mntl-text-block text-label-300 global-link")
    food_reviews = food_review.text.strip() if food_review else "No"

    food_photo = soup.find('div',class_ = "comp recipe-review-bar__photo-count mntl-text-block text-label-300 global-link dialog-link")
    food_photos = food_photo.text.strip() if food_photo else 'No'

    food_data = {
        'Food_Recipes':food_recipes,
        'Food_Ratings':food_ratings,
        'Food_Reviews':food_reviews,
        'Food_Photos':food_photos,
        'full_links':link
    }
    productitem.append(food_data)

df = pd.DataFrame(productitem)
df.to_csv('allrecipes.csv',index=False)
print(df)