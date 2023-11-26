import openpyxl
import os
import time
from selenium import webdriver
import openpyxl
import io
import pandas as pd
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import logging


class Scraper:

    def __init__(self, href, site_name, xpathes_dict):
        self.href = href
        self.dict_for_traders = {'Объем': [],
                                 'Валютная пара': [],
                                 'Тип сделки': [],
                                 'Время Открытия': [],
                                 'Цена Открытия': [],
                                 'Время Закрытия': [],
                                 'Цена Закрытия': [],
                                 'Прибыль': [],
                                 }
        self.months_in_numbers = {"янв.": "01",
                                  "февр.": "02",
                                  "мар.": "03",
                                  "апр.": "04",
                                  "мая": "05",
                                  "июня": "06",
                                  "июля": "07",
                                  "авг.": "08",
                                  "сент.": "09",
                                  "окт.": "10",
                                  "нояб.": "11",
                                  "дек.": "12",
                                  }
        self.site_name = site_name
        self.xpathes_dict = xpathes_dict

    def site_open(self):
        print(f'Перехожу по ссылке трейдера: {self.href.value}\n')
        options = webdriver.ChromeOptions()
        options.add_argument('chromedriver_binary.chromedriver_filename')
        # options.add_argument('headless')
        options.add_argument("window-size=1920,1080")
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()
        self.driver.get(self.href.value)
        print(f'Успешно перешел по ссылке {self.href.value}\n')
        try:
            WebDriverWait(self.driver, 20).until(
                ec.presence_of_element_located(
                    ("xpath", self.xpathes_dict['trader_name']))
            )
        except:
            logging.error(f'Проверьте, существует ли трейдер! Не смог найти имя трейдера по ссылке {self.href.value}')
            return None
        name = remove_special_chars(self.driver.find_element(
            "xpath",
            self.xpathes_dict['trader_name']).text)
        print(f'Имя трейдера = {name}\n')
        excel_name = fr'{bd_dir}\{self.site_name}\excel\{name}.xlsx'
        htm_name = fr'{bd_dir}\{self.site_name}\htm\{name}.htm'

    def site_scrap(self):
        pass

    def excel_save(self):
        pass

    def htm_save(self):
        pass

    def scrap_all(self):
        open_dict = self.site_open()
        self.site_scrap()
        self.excel_save()
        self.htm_save()


class Lifefinance(Scraper):
    def site_scrap(self):
        for o in (range(2, 10)):
            time.sleep(2)
            count = 0
            while count == 0:
                count = len(self.driver.find_elements("xpath",
                                                 fr'//div[@class = "content_row"]'))
            print(f'Начинаю обработку {count} записей на странице {o - 1}\n')
            for l in list(range(count - 49, count + 1)):
                currency = self.driver.find_element("xpath",
                                               fr'(//div[@class = "content_row"])[{l}]/descendant::a[2]').text
                if currency is not None:
                    date_close = self.driver.find_element("xpath",
                                                     fr'(//div[@class = "content_row"])[{l}]'
                                                     fr'/descendant::div[@class = "content_col"][3]').text
                    date_close = datetime.strptime(date_close,
                                                   '%d.%m.%Y %H:%M:%S') + timedelta(
                        hours=-1)
                    date_open = self.driver.find_element("xpath",
                                                    fr'(//div[@class = "content_row"])[{l}]'
                                                    fr'/descendant::div[@class = "content_col"][2]').text
                    date_open = datetime.strptime(date_open,
                                                  '%d.%m.%Y %H:%M:%S') + timedelta(
                        hours=-1)
                    type_of_trade = self.driver.find_element("xpath",
                                                        fr'(//div[@class = "content_row"])[{l}]'
                                                        fr'/descendant::div[@class = "content_col"][4]'
                                                        ).text.lower()
                    if type_of_trade == 'покупка':
                        type_of_trade = 'buy'
                    else:
                        type_of_trade = 'sell'
                    obj = self.driver.find_element("xpath",
                                              fr'(//div[@class = "content_row"])[{l}]'
                                              fr'/descendant::div[@class = "content_col"][5]'
                                              ).text.replace(".", ",")
                    currency = self.driver.find_element("xpath",
                                                   fr'(//div[@class = "content_row"])[{l}]/descendant::a[2]') \
                        .text.replace("XAUUSD", "GOLD")
                    price_open = self.driver.find_element("xpath",
                                                     fr'(//div[@class = "content_row"])[{l}]'
                                                     fr'/descendant::div[@class = "content_col"][6]'
                                                     ).text.replace(" ", "")
                    price_close = self.driver.find_element("xpath",
                                                      fr'(//div[@class = "content_row"])[{l}]'
                                                      fr'/descendant::div[@class = "content_col"][7]'
                                                      ).text.replace(" ", "")
                    points = self.driver.find_element("xpath",
                                                 fr'(//div[@class = "content_row"])[{l}]'
                                                 fr'/descendant::div[@class = "content_col"][8]'
                                                 ).text.replace(".", ",")
                    df_for_trader.loc[len(df_for_trader.index)] = [
                        obj,
                        currency,
                        type_of_trade,
                        date_open.strftime('%Y.%m.%d %H:%M'),
                        price_open,
                        date_close.strftime('%Y.%m.%d %H:%M'),
                        price_close,
                        points,
                    ]
            driver.execute_script("arguments[0].scrollIntoView();",
                                  driver.find_element("xpath",
                                                      fr'(//div[@class = "content_row"])[{count}]'))
        driver.quit()


class Forex4you(Scraper):
    pass


def make_hrefs_list(hrefs_file):
    input_excel = openpyxl.load_workbook(hrefs_file)
    sheet = input_excel['Лист1']
    list_of_input_hrefs = sheet['A']
    return list_of_input_hrefs


def remove_special_chars(string):
    pattern = r'[^\w\s]'
    return re.sub(pattern, '', string)


logging.basicConfig(
    level=logging.ERROR,
    filename='main.log',
    datefmt='%d.%m.%Y %H:%M:%S',
    filemode='w',
    format='%(asctime)s, %(levelname)s, %(message)s'
)

current_dir = os.path.dirname(os.path.abspath(__file__))
bd_dir = current_dir + r'\resources\БАЗА ДАННЫХ'
input_lists = [
    make_hrefs_list(bd_dir + r'\litefinance hrefs.xlsx'),
    make_hrefs_list(bd_dir + r'\forex4you hrefs.xlsx')
]
lifefinance_xpathes = {
    'trader_name': fr'//div[@class = "page_header_part traders_body"]//h2',
    'count': fr'//div[@class = "content_row"]',
    'currency': fr'(//div[@class = "content_row"])[{l}]/descendant::a[2]'
}

for site in input_lists:
    for href in site:
        if href is None:
            continue
        elif 'forex4you' in href.value:
            pass
        elif 'litefinance' in href.value:
            litefinance = Lifefinance(href, 'litefinance', lifefinance_xpathes)
            litefinance.scrap_all()
