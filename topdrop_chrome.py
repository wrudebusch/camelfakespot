#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

timestamp = str(time.time()).split(".")[0]
print(timestamp)


def get_top_drop(html_soup):
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


big = pd.DataFrame()
for page_num in range(1, 11):
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver")
    driver.get(f"https://camelcamelcamel.com/top_drops?p={page_num}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    new_df = get_top_drop(soup)
    big = big.append(new_df, ignore_index=True)

big.to_csv(f"top_drops_{timestamp}.csv", index=False)
