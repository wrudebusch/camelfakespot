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
            #print(str(other_prices))
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
                        .split("$")[1].split("<")[0]
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


def get_grade(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    review_div = soup.find_all("div", {"class": "review-grade"})
    grade = str(review_div[0]).split("<p>")[1].split("</p>")[0]
    return grade


def run_fakespot(item_id):
    driver = webdriver.Chrome("/snap/bin/chromium.chromedriver")
    driver.get("https://www.fakespot.com/")
    amazon_url = "https://www.amazon.com/dp/" + item_id
    search_box = driver.find_element_by_id("url-input-home")
    search_box.send_keys(amazon_url)
    search_button = driver.find_element_by_name("button")
    time.sleep(1)
    search_button.click()
    time.sleep(5)
    try:
        fakespot_grade = get_grade(driver.page_source)
    except:
        try:
            time.sleep(60)
            fakespot_grade = get_grade(driver.page_source)
        except:
            fakespot_grade = "0"
            print("error: " + amazon_url)
    driver.quit()
    return fakespot_grade


big = pd.DataFrame()
for page_num in range(3, 4):
    driver = webdriver.Chrome("/snap/bin/chromium.chromedriver")
    driver.get(f"https://camelcamelcamel.com/top_drops?p={page_num}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    new_df = get_top_drop(soup)
    big = big.append(new_df, ignore_index=True)

big.to_csv(f"top_drops_{timestamp}.csv", index=False)
#big["fs_grade"] = big["product_id"].map(lambda a: run_fakespot(a))
#big.to_csv(f"ccc_graded_{timestamp}.csv", index=False)