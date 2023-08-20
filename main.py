import requests
from bs4 import BeautifulSoup
import json

url = "http://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

quotes = []
for quote in soup.find_all("div", class_="quote"):
    text = quote.find("span", class_="text").get_text()
    author = quote.find("small", class_="author").get_text()
    tags = [tag.get_text() for tag in quote.find_all("a", class_="tag")]
    
    quotes.append({
        "tags": tags,
        "author": author,
        "quote": text
    })

with open("quotes.json", "w") as quotes_file:
    json.dump(quotes, quotes_file, indent=2)


authors = []
for author in soup.find_all("small", class_="author"):
    author_url = url + author.find_next("a")["href"]
    author_response = requests.get(author_url)
    author_soup = BeautifulSoup(author_response.text, "html.parser")
    
    name = author.get_text()
    born_date = author_soup.find("span", class_="author-born-date").get_text()
    born_location = author_soup.find("span", class_="author-born-location").get_text()
    description = author_soup.find("div", class_="author-description").get_text().strip()
    
    authors.append({
        "fullname": name,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    })

with open("authors.json", "w") as authors_file:
    json.dump(authors, authors_file, indent=2)
