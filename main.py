import requests
from bs4 import BeautifulSoup
url = "https://bodysize.org/en"

url_request = requests.get(url)
soup = BeautifulSoup(url_request.text, 'html.parser')

print(soup)