import requests
from bs4 import BeautifulSoup
url = "https://bodysize.org/en"

url_request = requests.get(url)
soup = BeautifulSoup(url_request.text, 'html.parser')

def get_person_data(soup):
    persons_ul = soup.find('ul', class_='persons')
    if persons_ul:
        persons_ul_li = persons_ul.find_all('li')
        list_items = []

        for person in persons_ul_li:
            name_link = person.find('a', class_='name')
            if name_link:
                list_items.append(name_link)

        return list_items
    return []

first_page_items = get_person_data(soup)
print(first_page_items)