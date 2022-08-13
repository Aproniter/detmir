import csv
import argparse
from unicodedata import category

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


MAX_WAIT = 3


def csv_create(catalog, category):
    with open(f'{category}.csv', 'w', newline='') as file:
        fieldnames = ['id', 'title', 'price', 'promo_price', 'url']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in catalog:
            writer.writerow(catalog[row])


def detmir(category):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166")
    options.add_argument('--window-size=1366,768')
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    wait = WebDriverWait(driver, MAX_WAIT)
    catalog = {}    
    for page in range(1, 100):
        driver.get(f'https://www.detmir.ru/catalog/index/name/{category}/page/{page}/')
        try:
            products = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'aside'))).find_elements(By.XPATH, '../div/div')[-1]
        except TimeoutException:
            continue
        try:
            products = products.find_elements(By.CSS_SELECTOR, 'a')
            
            for product in products:
                content = product.text.split('\n')
                url = product.get_attribute('href')
                id = url.split('/')[-2]
                title = ''
                price = 0
                promo_price = 0

                if content[-1] == 'Нет в наличии':
                    if content[-2].isdigit():
                        title = content[-3]
                    else:
                        title = content[-2]
                elif content[-1].find('₽') != -1:
                    price = int(content[-1].replace(' ₽', '').replace(u'\u2009', ''))
                    if content[-2].find('₽') != -1:
                        promo_price = int(content[-2].replace(' ₽', '').replace(u'\u2009', ''))
                        if content[-3].isdigit():
                            title = content[-4]
                        else:
                            title = content[-3]
                    elif content[-2].isdigit():
                        title = content[-3]
                    else:
                        title = content[-2]
                catalog.update({
                    title: {
                        'title': title,
                        'id': id,
                        'price': price,
                        'promo_price': promo_price,
                        'url': url
                    }
                })
        except StaleElementReferenceException:
            continue
    csv_create(catalog, category)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Выбор категории')
    parser.add_argument('-c', '--category', dest='category', required=True)
    args = parser.parse_args()
    category = args.category
    detmir(category)
