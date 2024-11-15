import requests
from bs4 import BeautifulSoup
import csv

url = "https://bodysize.org/tr"

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

def write_to_csv(data):
    with open('output.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Ad', 'Boy', 'Ağırlık'])  # Başlık satırı

        for entry in data:
            writer.writerow(entry)

first_page_items = get_person_data(soup)
all_person_data = []

for item in first_page_items:
    name = item.text.strip()  # Extract the name of the person from the link text
    new_href = item['href'].replace('/tr/', '/')  # Fix the URL to match the correct path
    person_url = url + new_href  # Construct the full URL for the person's page

    person_page = requests.get(person_url)  # Send a request to the person's page
    person_soup = BeautifulSoup(person_page.text, 'html.parser')  # Parse the HTML of the person's page

    # Find height and weight
    height = None
    weight = None
    rows = person_soup.find_all('tr')  # Find all rows in the table
    for row in rows:
        header = row.find('th')  # Find the header (e.g., "Height" or "Weight")
        data = row.find('td')  # Find the data associated with the header
        if header and data:
            if "Boy" in header.text:  # Check if the header contains "Boy" (height)
                height = data.text.strip()  # Extract the height value
            elif "Ağırlık" in header.text:  # Check if the header contains "Ağırlık" (weight)
                weight = data.text.strip()  # Extract the weight value

    all_person_data.append([name, height, weight])  # Add the person's data to the list

for page in range(2, 2443):
    page_url = f"https://bodysize.org/tr/page/{page}/"
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    list_items = get_person_data(soup)

    for item in list_items:
        name = item.text.strip()
        new_href = item['href'].replace('/tr/', '/')
        person_url = url + new_href

        person_page = requests.get(person_url)
        person_soup = BeautifulSoup(person_page.text, 'html.parser')

        # Boy ve Ağırlığı bul
        height = None
        weight = None
        rows = person_soup.find_all('tr')
        for row in rows:
            header = row.find('th')
            data = row.find('td')
            if header and data:
                if "Boy" in header.text:
                    height = data.text.strip()
                elif "Ağırlık" in header.text:
                    weight = data.text.strip()

        all_person_data.append([name, height, weight])

write_to_csv(all_person_data)
print("Data saved in output.csv file.")