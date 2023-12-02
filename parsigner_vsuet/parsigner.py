import time

from bs4 import BeautifulSoup
import requests
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

headers_of_partners = [
    'Наименование организации', 'Предмет договора', 'Ссылка на сайт'
]


# парсим партнерскую программу
def get_partners(url: str) -> list:
    response = requests.get(url=url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    data = []
    i = 1
    for company in soup.find_all('tr'):
        if company.get('itemprop'):
            name = company.find('td')
            low = name.find_next_sibling()
            site = low.find_next_sibling()
            data.append([name.text.strip(), low.text.strip(), site.find('a').get('href')])
        else:
            continue

    return data


# сохраняем партнерскую программу в .csv файл
with open('partners.csv', 'a', encoding='utf-8-sig', newline='') as file:
    writer_partners = csv.writer(file, delimiter=';')
    writer_partners.writerow(
        headers_of_partners
    )

    data_partners = get_partners("https://vsuet.ru/science/iop/nashi_partners")

    for row in data_partners:
        writer_partners.writerow(
            row
        )

# парсим .pdf файл
with webdriver.Chrome() as browser:
    browser.get(url="https://vsuet.ru/abitur/magistr")
    # domain = 'https://vsuet.ru'
    # browser.find_elements(By.CLASS_NAME, 'svoo-row')[1].send_keys(Keys.TAB)