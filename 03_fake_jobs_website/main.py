import requests
import pandas as pd
from bs4 import BeautifulSoup

fake_jobs = []

website = "https://realpython.github.io/fake-jobs/"
r = requests.get(website)
soup = BeautifulSoup(r.content, "html.parser")

card_content = soup.find_all("div",class_ = "card-content")

for item in card_content:
    title = item.find("h2",class_ = "title is-5").text.strip()
    comapany = item.find("h3",class_ = "subtitle is-6 company").text.strip()
    location = item.find("p",class_ = "location").text.strip()
    time = item.find("time").text.strip()
    footer = item.find("footer",class_ = "card-footer").text.strip()
    footer_link = item.find("a")["href"]

    fake_jobs_data = {
        "Title": title,
        "Company": comapany,
        "Location": location,
        "Time": time,
        "Footer": footer,
        "Footer Link": footer_link
    }
    fake_jobs.append(fake_jobs_data)

df = pd.DataFrame(fake_jobs)
df.to_csv("03_fake_jobs.csv",index = False)    