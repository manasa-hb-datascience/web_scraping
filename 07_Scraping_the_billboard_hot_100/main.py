import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

product_data = []


baseurl = "https://www.billboard.com"

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36'
}

url = f"https://www.billboard.com/charts/hot-100/"
r = requests.get(url,headers=headers)

soup = BeautifulSoup(r.content,"html.parser")

songs = soup.find_all("div", class_="o-chart-results-list-row-container")


for song in songs:
    title = song.find('h3')
    artist = song.find('span')
    link_tag = song.find("a",href = True)
    
    if title and artist and link_tag:
        full_link = baseurl + link_tag['href']
        
        song_dict = {
            "Title": title.text.strip(),
            "Artist" : artist.text.strip(),
            "Link": full_link
        }
        product_data.append(song_dict)

df = pd.DataFrame(product_data)
df.to_csv("songs_playlist.csv",index = False)