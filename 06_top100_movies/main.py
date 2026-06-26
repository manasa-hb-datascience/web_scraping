import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://www.empireonline.com/movies/features/best-movies-2/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Page loaded successfully!")
else:
    print(f"Failed to load page. Status code: {response.status_code}")

soup = BeautifulSoup(response.text, "html.parser")

movie_list = []

for tag in soup.find_all("h2"):
    text = tag.get_text(strip=True)

    # Match movie entries like "100) Avatar (2009)"
    if re.match(r'^\d+\)', text):

        rank = text.split(")")[0]
        movie_name = text.split(")", 1)[1].strip()

        movie_list.append({
            "Rank": int(rank),
            "Movie": movie_name
        })

# Sort from Rank 1 to Rank 100
movie_list = sorted(movie_list, key=lambda x: x["Rank"])

df = pd.DataFrame(movie_list)

df.to_csv("top100_movies.csv", index=False, encoding="utf-8")

print(f"Found {len(df)} movies")
print("CSV file saved successfully!")