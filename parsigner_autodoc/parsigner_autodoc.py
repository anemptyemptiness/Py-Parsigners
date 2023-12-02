import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


login = 'ADL-56976'
password = '501A3559'


def parser() -> None:
    with open("autodoc.csv", "w", encoding="utf-8-sig", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(
            ['Бренд', 'Наименование детали', 'Цена (в рублях)', 'Срок доставки (в днях)']
        )

    with webdriver.Chrome() as browser:
        browser.get(url='https://www.autodoc.ru/')

        # переходим в личный кабинет
        actions = ActionChains(browser)
        for _ in range(12):
            actions = actions.send_keys(Keys.TAB)
        actions.send_keys(Keys.ENTER).perform()

        login_input_locator = (By.ID, 'login-screen-form')
        password_input_locator = (By.CLASS_NAME, 'password-form')

        wait = WebDriverWait(browser, 10)
        login_input = wait.until(EC.presence_of_element_located(login_input_locator))
        password_input = wait.until(EC.presence_of_element_located(password_input_locator))

        if login_input.is_displayed():
            login_input.find_element(By.TAG_NAME, 'input').send_keys(login)
            password_input.find_element(By.TAG_NAME, 'input').send_keys(password)
            browser.find_element(By.ID, 'submit_logon_page').click()
        time.sleep(2)

        # переходим в каталоги
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'title')))
        category_url = browser.find_element(By.CLASS_NAME, 'title').get_attribute('href')

        browser.get(f'{category_url}')

        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'p-dropdown')))
        choice = browser.find_element(By.TAG_NAME, 'p-dropdown')
        choice.click()
        WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'p-dropdownitem')))
        browser.find_element(By.TAG_NAME, 'p-dropdownitem').click()
        time.sleep(3)

        # переходим в Оригинальные запчасти
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'catalogs-container')))
        url = browser.find_element(By.CLASS_NAME, 'catalogs-container').find_element(By.TAG_NAME, 'a').get_attribute('href')
        browser.get(f'{url}')

        # ищем "Ролик натяжной"
        url = ''
        if WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'one-node'))):
            for category in browser.find_elements(By.TAG_NAME, 'one-node'):
                if not url:
                    if category.text == 'Двигатель':
                        category.click()
                        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
                        for mechanism_gas in browser.find_elements(By.TAG_NAME, 'p-treenode'):
                            if mechanism_gas.text == 'Механизм газораспределения':
                                mechanism_gas.click()
                                WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
                                for grm in browser.find_elements(By.TAG_NAME, 'li'):
                                    if grm.text == 'Ремень ГРМ, натяжители ремня':
                                        grm.click()
                                        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'ul')))
                                        for tension_roller in browser.find_elements(By.TAG_NAME, 'li'):
                                            if tension_roller.text == 'Ролик натяжителя':
                                                tension_roller.click()
                                                WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, '//button[@class="button button-red"]'))).click()
                                                url = browser.current_url
                                                break
                                        break
                                break
                        break
                else:
                    break

        browser.get(f"{url}")
        time.sleep(2)

        # переходим к ассортименту
        [x for x in browser.find_elements(By.CLASS_NAME, 'table-detail')][2].find_elements(By.TAG_NAME, 'a')[1].click()
        url = browser.current_url
        browser.get(f'{url}')
        time.sleep(2)

        browser.switch_to.window(browser.window_handles[1])

        # создаем списки, для их заполнения необходимой информацией
        brands = []
        names = []
        prices = []
        delivery = []
        data = []

        time.sleep(2)
        # собираем все натяжные ролики
        for product in browser.find_elements(By.XPATH, '//div[@class="pro-header ng-star-inserted"]'):
            if len(delivery) > 3:
                brands.append(product.find_element(By.CLASS_NAME, 'title-part').text if product.find_element(By.CLASS_NAME, 'title-part').text else "Не указано")
                names.append(product.find_element(By.CLASS_NAME, 'title-name').text if product.find_element(By.CLASS_NAME, 'title-name').text else "Не указано")
                prices.append(product.find_element(By.CLASS_NAME, 'start-price').text.strip('\n2.0') if product.find_element(By.CLASS_NAME, 'start-price').text else "Не указано")
                delivery.append("Уточните у продавца")
                ActionChains(browser).scroll_by_amount(0, 300).perform()
            else:
                brands.append(product.find_element(By.CLASS_NAME, 'title-part').text)
                names.append(product.find_element(By.CLASS_NAME, 'title-name').text)
                prices.append(product.find_element(By.CLASS_NAME, 'start-price').text.strip('\n'))
                delivery.append(product.find_element(By.CLASS_NAME, 'delivery-number').text)
                ActionChains(browser).scroll_by_amount(0, 300).perform()

        for i in range(len(brands)):
            data.append([brands[i], names[i], prices[i], delivery[i]])

        # записываем в .csv файл
        for row in data:
            with open('autodoc.csv', 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    row
                )


if __name__ == '__main__':
    try:
        parser()
        print('Работа завершена! Файл .csv успешно записан')
    except:
        print('Что-то пошло не так')
