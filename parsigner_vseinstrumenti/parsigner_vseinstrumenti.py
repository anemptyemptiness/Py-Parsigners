from selenium import webdriver
from bs4 import BeautifulSoup
import csv

DOMAIN = 'https://spb.vseinstrumenti.ru'


def parser_tools(urls) -> None:
    for url in urls:
        with webdriver.Chrome() as browser:
            browser.get(url)
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            data = []

        if len(soup.find_all(class_='number')) > 1:
            pagen = [f"{url}page{x}/" for x in range(1, int(soup.find_all(class_='number')[-1].text) + 1)]
            pagen[0] = url
        else:
            pagen = [url]

        for pagen_item in pagen:
            with webdriver.Chrome() as browser:
                browser.get(url=pagen_item)
                html = browser.page_source
                soup = BeautifulSoup(html, "html.parser")
                articles = [x.find('p', attrs={'data-qa': 'product-code-text'}).text.strip()
                            if x.find('p', attrs={'data-qa': 'product-code-text'})
                            else "Нет информации"
                            for x in soup.find_all('div', class_='LXySrk')]
                names = [x.find('a', attrs={'data-qa': 'product-name'}).get('title')
                         if x.find('a', attrs={'data-qa': 'product-name'})
                         else "Нет информации"
                         for x in soup.find_all('div', class_='LXySrk')]
                prices = [x.find('p', attrs={'data-qa': 'product-price-current'}).text.strip('&nbsp;')
                          if x.find('p', attrs={'data-qa': 'product-price-current'})
                          else "Нет информации"
                          for x in soup.find_all('div', class_='LXySrk')]
                availabilities = [x.find('p', attrs={'data-qa': 'product-availability-total-available'}).text
                                  if x.find('p', attrs={'data-qa': 'product-availability-total-available'})
                                  else "Нет в наличии"
                                  for x in soup.find_all('div', class_='LXySrk')]
                links_to_item = [
                    "https://spb.vseinstrumenti.ru" + x.find('a', attrs={'data-qa': 'product-name'}).get('href')
                    if x.find('a', attrs={'data-qa': 'product-name'})
                    else "Нет информации"
                    for x in soup.find_all('div', class_='LXySrk')]

                for i in range(len(articles)):
                    data.append([articles[i], names[i], prices[i], availabilities[i], links_to_item[i]])

        with open(f"{url.split('/')[4]}.csv", "w", encoding="utf-8-sig", newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                ['Артикул', 'Наименование', 'Цена', 'Наличие', 'Ссылка на товар']
            )

        for row in data:
            with open(f"{url.split('/')[4]}.csv", 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    row
                )

        data.clear()
        pagen.clear()


def get_tools_urls() -> list:
    with webdriver.Chrome() as browser:
        browser.get("https://spb.vseinstrumenti.ru/category/stroitelnyj-instrument-6474/")
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        urls = [DOMAIN + x.find('a').get('href') for x in soup.find_all(class_='_5uKBsp xpfZ5m')]

    return urls


def get_accum_urls(url: str, tag: str = None) -> list:
    with webdriver.Chrome() as browser:
        browser.get(url=url)
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        urls = [DOMAIN + x.find('a').get('href') for x in soup.find_all(class_=f'{tag}')]

    return urls


if __name__ == '__main__':
    urls_tools = get_tools_urls()
    # parser_tools(get_accum_urls(urls_tools[0]))  # Аккумуляторный инструмент
    # parser_tools(urls_tools[1:2])  # Болгарки (ушм)
    # print("Болгарки выполнены")
    # parser_tools(urls_tools[2:3])  # Гайковерты
    # parser_tools(get_accum_urls(urls_tools[3], "QQR-Wc xpfZ5m CQQqRL"))  # Генераторы
    # print("Генераторы выполнены")
    # parser_tools(get_accum_urls(urls_tools[4], "QQR-Wc xpfZ5m CQQqRL"))  # Граверы
    # print("Граверы выполнены")
    # parser_tools(get_accum_urls(urls_tools[5], "QQR-Wc xpfZ5m CQQqRL"))  # Дрели
    # print("Дрели выполнены")
    # parser_tools(get_accum_urls(urls_tools[6], "QQR-Wc xpfZ5m CQQqRL"))  # Заклепочники
    # print("Заклепочники выполнены")
    # parser_tools(get_accum_urls(urls_tools[7], "_5uKBsp xpfZ5m"))  # Измерительные приборы
    # print("Измерительные приборы выполнены")
    # parser_tools(get_accum_urls(urls_tools[8], "_5uKBsp xpfZ5m"))  # Инструмент и оборудование по видам работ
    # print("Инструменты и оборудование по видам работ выполнены")
    # parser_tools(urls_tools[9:10])  # Клуппы электрические
    # print("Клупы электрические выполнены")
    # parser_tools(get_accum_urls(urls_tools[10], "_5uKBsp xpfZ5m"))  # Компрессоры
    # print("Компрессоры выполнены")
    # parser_tools(get_accum_urls(urls_tools[11], "_5uKBsp xpfZ5m"))  # Краскопульты
    # print("Краскопульты выполнены")
    # parser_tools(urls_tools[12:13])  # Электролобзики
    # print("Электролобзики выполнены")
    # parser_tools(get_accum_urls(urls_tools[13], "_5uKBsp xpfZ5m"))  # Многофункциональные реноваторы
    # print("Многофункциональные реноваторы выполнены")
    # parser_tools(get_accum_urls(urls_tools[14], "_5uKBsp xpfZ5m"))  # Наборы инструментов
    # print("Наборы инструментов выполнены")
    # parser_tools(get_accum_urls(urls_tools[15], "_5uKBsp xpfZ5m"))  # Электрические ножницы
    # print("Электрические ножницы выполнены")
    # parser_tools(get_accum_urls(urls_tools[16], "QQR-Wc xpfZ5m CQQqRL"))  # Отбойные молотки
    # print("Отбойные молотки выполнены")
    # parser_tools(get_accum_urls(urls_tools[17], "_5uKBsp xpfZ5m"))  # Паяльное оборудование
    # print("Паяльное оборудование выполнено")
    # parser_tools(get_accum_urls(urls_tools[18], "_5uKBsp xpfZ5m"))  # Перфораторы
    # print("Перфораторы выполнены")
    # parser_tools(get_accum_urls(urls_tools[19], "QQR-Wc xpfZ5m CQQqRL"))  # Пилы строительные
    # print("Пилы строительные выполнены")
    # parser_tools(get_accum_urls(urls_tools[20], "QQR-Wc xpfZ5m CQQqRL"))  # Пистолеты
    # print("Пистолеты выполнены")
    # parser_tools(get_accum_urls(urls_tools[21], "QQR-Wc xpfZ5m CQQqRL"))  # Пневмоинструмент
    # print("Пневмоинструменты выполнены")
    # parser_tools(get_accum_urls(urls_tools[22], "_5uKBsp xpfZ5m"))  # Пневмоподготовка
    # print("Пневмоподготовка выполнена")
    # parser_tools(urls_tools[23:24])  # Пневмошуруповерт
    # print("Пневношуруповерты выполнены")
    # parser_tools(get_accum_urls(urls_tools[24], "QQR-Wc xpfZ5m CQQqRL"))  # Сварочное оборудование
    # print("Сварочное оборудование выполнено")
    # parser_tools(urls_tools[25:26])  # Степлеры строительные
    # print("Степлеры строительные выполнены")
    # parser_tools(urls_tools[26:27])  # Пылесосы строительные
    # print("Пылесосы строительные выполнены")
    # parser_tools(get_accum_urls(urls_tools[27], "_5uKBsp xpfZ5m"))  # Строительные и промышленные фены
    # print("Строительные и промышленные фены выполнены")
    # parser_tools(get_accum_urls(urls_tools[28], "_5uKBsp xpfZ5m"))  # Фрезеры
    # print("Фрезеры выполнены")
    # parser_tools(get_accum_urls(urls_tools[29], "QQR-Wc xpfZ5m CQQqRL"))  # Шлифовальные машинки
    # print("Шлифовальные машинки выполнены")
    # parser_tools(urls_tools[30:31])  # Штроборезы
    # print("Штроборезы выполнены")
    # parser_tools(get_accum_urls(urls_tools[31], "QQR-Wc xpfZ5m CQQqRL"))  # Шуруповерты
    # print("Шуруповерты выполнены")
    # parser_tools(urls_tools[32:33])  # Электрорубанки
    # print("Электрорубанки выполнены")

