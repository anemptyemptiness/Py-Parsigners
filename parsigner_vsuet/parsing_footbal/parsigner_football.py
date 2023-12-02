import time

import aiohttp
from bs4 import BeautifulSoup
import asyncio
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint


async def parser(url: str):
    if url == 'http://chertanovo-camp.ru/#contacts':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                address = soup.find('div', class_='listprem').find_all('p')[0].text.strip("Адрес: ")
                phone = soup.find('div', class_='listprem').find_all('p')[1].text.strip("Телефон: ")
                email = soup.find('div', class_='listprem').find_all('p')[2].text.strip("E-mail: \n")

                data.append([address, phone, email, url])

                with open("chertanovo-camp.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Адрес', 'Телефон', 'E-mail', 'Ссылка на сайт', ]
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'http://chertanovoclub.com/about/contacts':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                # Парсинг Приемной директора
                title = soup.find_all('div', class_='card shadow-sm text-center mb-2')[0].find_all('strong')[0].text.strip()
                phone_director = soup.find_all('div', class_='card shadow-sm text-center mb-2')[0].find_all('p', class_='card-text')[0].text.strip("Телефон: ")
                email_director = soup.find_all('div', class_='card shadow-sm text-center mb-2')[0].find_all('p', class_='card-text')[1].text.strip("E-mail: ")
                address = soup.find('h4', class_='text-center mb-2').text.strip()

                data.append([address, title, phone_director, email_director, 'Нет информации', url])

                # Парсинг Аренды полей
                title = soup.find_all('div', class_='card shadow-sm text-center mb-2')[3].find_all('strong')[0].text.strip()
                phone_director = soup.find_all('div', class_='card shadow-sm text-center mb-2')[3].find_all('p', class_='card-text')[0].text.strip("Телефон: ")
                email_director = soup.find_all('div', class_='card shadow-sm text-center mb-2')[3].find_all('p', class_='card-text')[1].text.strip(" ")
                press_attashe = soup.find_all('div', class_='card shadow-sm text-center mb-2')[3].find_all('p', class_='card-text')[2].text.strip("Пресс-атташе: ")

                data.append([address, title, phone_director, email_director, press_attashe, url])

                with open("chertanovoclub.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Адрес', 'Заголовок', 'Телефон', 'E-mail', 'Пресс-атташе', 'Ссылка на сайт', ]
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'https://fckrasnodar.ru/club/contacts/':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                address = soup.find('section', id='content').find_all('dl', class_='data')[0].find('dd').text.strip()
                post_office = soup.find('section', id='content').find_all('dl', class_='data')[1].find('dd').text.strip()
                club_requisites = soup.find('section', id='content').find_all('dl', class_='data')[2].find('dd').find('a').get('href')
                phone = soup.find('section', id='content').find_all('dl', class_='data')[3].find('dd').text.strip()
                fax = soup.find('section', id='content').find_all('dl', class_='data')[4].find('dd').text.strip()
                socials = [x.get('href') for x in soup.find('dd', class_='social-links').find_all('a')]

                data.append([address, post_office, club_requisites, phone, fax, socials, url])

                with open("fckrasnodar.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Адрес', 'Для почтовых отправлений', 'Реквизиты клуба', 'Телефон', 'Факс', 'Соцсети', 'Ссылка на сайт', ]
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'https://footbolika.ru/raspisanie/':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                for item in soup.find_all('div', class_='row office-row'):
                    phone = item.find('div', class_='phone').find('a').get('href')

                    if "Мы Вконтакте" in item.text:
                        vk = item.find('div', class_='link-vk').find('a').get('href')
                    else:
                        vk = "Нет информации"

                    if "whatsapp" in item.find('ul', class_='social').text:
                        whatsapp = item.find('ul', class_='social').find('li', class_='whatsapp').find('a').get('href')
                    else:
                        whatsapp = "Нет информации"

                    if "инстаграм" in item.find('ul', class_='social').text:
                        instagram = item.find('li', class_='instagram').find('a').get('href')
                    else:
                        instagram = 'Нет информации'

                    data.append([phone, vk, whatsapp, instagram])

                with open("footbolika-saint-petersburg.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Телефон', 'ВКонтакте', 'WhatsApp', 'Instagram']
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'https://msk.footbolika.ru/raspisanie/':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                for item in soup.find_all('div', class_='row office-row'):
                    phone = item.find('div', class_='phone').find('a').get('href')
                    if "Мы Вконтакте" in item.text:
                        vk = item.find('div', class_='link-vk').find('a').get('href')
                    else:
                        vk = "Нет информации"

                    if "whatsapp" in item.find('ul', class_='social').text:
                        whatsapp = item.find('ul', class_='social').find('li', class_='whatsapp').find('a').get('href')
                    else:
                        whatsapp = "Нет информации"

                    if "инстаграм" in item.find('ul', class_='social').text:
                        instagram = item.find('li', class_='instagram').find('a').get('href')
                    else:
                        instagram = 'Нет информации'

                    data.append([phone, vk, whatsapp, instagram])

                with open("footbolika-moscow.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Телефон', 'ВКонтакте', 'WhatsApp', 'Instagram']
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'https://schoolfcdm.ru/':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                phone = soup.find('div', attrs={'data-elem-id': '1683984101160'}).find('a').get('href')
                telegram = soup.find('div', attrs={'data-elem-id': '1683984151734'}).find('a').get('href')
                vk = soup.find('div', attrs={'data-elem-id': '1683984161635'}).find('a').get('href')
                whatsapp = soup.find('div', attrs={'data-elem-id': '1683984101157'}).find('a').get('href')

                data.append([phone, telegram, vk, whatsapp, 'admin@schoolfcdm.ru', url])

                with open("schoolfcdm.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Телефон', 'Telegram', 'Вконтакте', 'WhatsApp', 'E-mail', 'Ссылка на сайт', ]
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'https://academy.spartak.com/contacts/':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                phone_1 = soup.find('div', class_='container __container').find_all('p')[2].text.strip("Тел: ")
                # email = soup.find('div', class_='container __container').find_all('p')[3].find('a').text

                data.append([phone_1, 'school@spartak.com', ' ', ' ', ' ', ' ', ' ', url, ])

                phone_2 = soup.find('div', class_='container __container').find_all('p')[17].text.strip("Тел: ")
                # email = soup.find('div', class_='container __container').find_all('p')[19].find('a').text

                vk = soup.find('div', class_='b_footer_social').find_all('a')[0].get('href')
                twitter = soup.find('div', class_='b_footer_social').find_all('a')[1].get('href')
                instagram = soup.find('div', class_='b_footer_social').find_all('a')[2].get('href')
                youtube_1 = soup.find('div', class_='b_footer_social').find_all('a')[3].get('href')
                youtube_2 = soup.find('div', class_='b_footer_social').find_all('a')[4].get('href')

                data.append([phone_2, 'sokolniki@spartak.com', vk, twitter, instagram, youtube_1, youtube_2, url, ])

                with open("academy_spartak.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Телефон', 'E-mail', 'Вконтакте', 'Twitter', 'Instagram', 'YouTube-1', 'YouTube-2', 'Ссылка на сайт']
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'https://academy.pfc-cska.com/school/information/contacts/':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                # phone = soup.find('div', class_='col-sm-9 page-content').find_all('b')[2].text
                email = soup.find('div', class_='col-sm-9 page-content').find_all('b')[3].find_next('a')
                vk = email.find_next('a')
                telegram = vk.find_next('a')
                rutube = soup.find('div', class_='social footer__social').find_all('a')[2].get('href')
                twitter = soup.find('div', class_='social footer__social').find_all('a')[3].get('href')

                data.append(["8 (499) 728-62-40", email, vk.text, telegram.text, rutube, twitter, url])

                with open("academy_pfc-cska.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Телефон', 'E-mail', 'Вконтакте', 'Telegram', 'Rutube', 'Twitter', 'Ссылка на сайт']
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'https://fc-zenit.ru/academy/academy_main/contact/':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                phone = soup.find('div', id='workarea').find_all('p')[1].text
                email = soup.find('div', id='workarea').find_all('p')[2].find('a').text
                vk = soup.find_all('ul', class_='footer-navblock')[2].find('a', string='ВКонтакте').get('href')
                twitter = soup.find_all('ul', class_='footer-navblock')[2].find('a', string='Твиттер').get('href')
                ok = soup.find_all('ul', class_='footer-navblock')[2].find('a', string='Одноклассники').get('href')
                youtube = soup.find_all('ul', class_='footer-navblock')[2].find('a', string='YouTube').get('href')

                data.append([phone, email, vk, twitter, ok, youtube, url])

                with open("fc-zenit.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Телефон', 'E-mail', 'Вконтакте', 'Twitter', 'Одноклассники', 'YouTube', 'Ссылка на сайт']
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )

    elif url == 'https://jufootball.ru/':
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = []

                soup = BeautifulSoup(await response.text(), 'lxml')
                phone = soup.find('div', 'header__phone').find('a').text
                email = soup.find('div', 'header__mail').find('a').text
                vk = soup.find('div', 'map-footer__btns').find_all('a', class_='grey-btn')[1].get('href')
                telegram = soup.find('div', 'map-footer__btns').find_all('a', class_='grey-btn')[2].get('href')

                data.append([phone, email, vk, telegram, url])

                with open("jufootball.csv", 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow(
                        ['Телефон', 'E-mail', 'Вконтакте', 'Telegram', 'Ссылка на сайт']
                    )

                    for row in data:
                        writer.writerow(
                            row
                        )


async def main():
    urls = ['http://chertanovo-camp.ru/#contacts',
            'http://chertanovoclub.com/about/contacts',
            'https://fckrasnodar.ru/club/contacts/',
            'https://footbolika.ru/raspisanie/',
            'https://msk.footbolika.ru/raspisanie/',
            'https://schoolfcdm.ru/',
            'https://academy.spartak.com/contacts/',
            'https://academy.pfc-cska.com/school/information/contacts/',
            'https://fc-zenit.ru/academy/academy_main/contact/',
            'https://jufootball.ru/',
            ]
    await asyncio.gather(*[parser(url) for url in urls])


if __name__ == '__main__':
    asyncio.run(main())
