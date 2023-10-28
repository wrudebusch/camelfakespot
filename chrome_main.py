#!/usr/bin/env python
# coding: utf-8

from utilities import *
import sys
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

timestamp = str(time.time()).split(".")[0]

my_option = sys.argv[1].strip().lower()

tic = datetime.now()
log_name = str(__file__).split(".")[0]
logging = get_logging(log_name)


def get_top_drop(html_soup):
    old = pd.DataFrame()
    card_div = soup.find_all("div", {"class": "card"})
    for card in card_div:
        try:
            product_info = card.select_one("a[href*=product]")
            other_prices = (
                card.find_all("div", {"class": "compare_price text-center"}),
            )
            current_price_raw = card.find_all(
                "div", {"class": "current_price text-center"}
            )
            new_df = pd.DataFrame.from_records(
                [
                    {
                        "current_price": str(current_price_raw)
                        .split(">")[1]
                        .split("</")[0]
                        .replace("$", "")
                        .strip(),
                        "previous_price": str(other_prices)
                        .split("Previous price:\n")[1]
                        .split(" </div>")[0]
                        .split("$")[1]
                        .split("<")[0]
                        .strip(),
                        "product_id": str(product_info)
                        .split("/product/")[1]
                        .split("?")[0],
                        "product_title": str(product_info)
                        .split("title=")[1]
                        .split(">")[0],
                        "page_num": str(page_num),
                        "timestamp": timestamp,
                    }
                ]
            )
            old = old.append(new_df, ignore_index=True)
        except:
            print("error")
    return old


def get_popular(html_soup):
    old = pd.DataFrame()
    card_div = soup.find_all("div", {"class": "card"})
    for card in card_div:
        try:
            product_info = card.select_one("a[href*=product]")
            other_prices = (
                card.find_all("div", {"class": "compare_price text-center"}),
            )
            current_price_raw = card.find_all(
                "div", {"class": "current_price text-center"}
            )
            new_df = pd.DataFrame.from_records(
                [
                    {
                        "current_price": str(current_price_raw)
                        .split(">")[1]
                        .split("</")[0]
                        .replace("$", "")
                        .strip(),
                        "list_price": str(other_prices)
                        .split("List price:\n")[1]
                        .split(" </div>")[0]
                        .replace("$", "")
                        .strip(),
                        "avg_price": str(other_prices)
                        .split("Average price:\n")[1]
                        .split(" </div>")[0]
                        .replace("$", "")
                        .strip(),
                        "product_id": str(product_info)
                        .split("/product/")[1]
                        .split("?")[0],
                        "product_title": str(product_info)
                        .split("title=")[1]
                        .split(">")[0],
                        "page_num": str(page_num),
                        "timestamp": timestamp,
                    }
                ]
            )
            old = old.append(new_df, ignore_index=True)
        except:
            print("error")
    return old


## this options are the same for both top_drop and popular ##

opts = webdriver.ChromeOptions()
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)
opts.add_argument("--disable-blink-features=AutomationControlled")

big = pd.DataFrame()

for page_num in range(1, 11):
    #try:
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service,options=opts)
    driver.get(f"https://camelcamelcamel.com/{my_option}?p={page_num}")
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,"//iframe[@title='Widget containing a Cloudflare security challenge']")))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//label[@class='ctp-checkbox-label']"))).click()
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    #print(soup)
    if my_option == 'top_drops':
        new_df = get_top_drop(soup)
    if my_option == 'popular':
        new_df = get_popular(soup)
    big = big.append(new_df, ignore_index=True)
    logging.info(f"{my_option} at page = {page_num}")
   # except:
   #     logging.error(f"{my_option} error")


big.to_csv(f"{my_option}.csv", index=False)

toc = datetime.now()
logging.info(my_option+ " total runtime: " + str(toc - tic))
