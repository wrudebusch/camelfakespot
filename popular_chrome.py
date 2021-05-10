#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

timestamp = str(time.time()).split(".")[0]
#print(timestamp)


def get_popular(html_soup):
    old = pd.DataFrame()
    card_div = soup.find_all("div", {"class": "card"})
    for card in card_div:
        try:
            product_info = card.select_one("a[href*=product]")
            other_prices = (
                card.find_all("div", {"class": "compare_price text-center"}),
            )
            curret_price_raw = card.find_all(
                "div", {"class": "current_price text-center"}
            )
            new_df = pd.DataFrame.from_records(
                [
                    {
                        "curret_price": str(curret_price_raw)
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

opts = webdriver.ChromeOptions()
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)
opts.add_argument("--disable-blink-features=AutomationControlled")

big = pd.DataFrame()
for page_num in range(1, 11):
    driver = webdriver.Chrome(options=opts, executable_path="/usr/bin/chromedriver")
    driver.get(f"https://camelcamelcamel.com/popular?p={page_num}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    new_df = get_popular(soup)
    big = big.append(new_df, ignore_index=True)

big.to_csv("popular.csv", index=False)
