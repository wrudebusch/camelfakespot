#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time

timestamp = str(time.time()).split(".")[0]
print(timestamp)


def get_grade(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    review_div = soup.find_all("div", {"class": "review-grade"})
    grade = str(review_div[0]).split("<p>")[1].split("</p>")[0]
    return grade


def run_fakespot(item_id):
    driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
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
            time.sleep(99)
            fakespot_grade = get_grade(driver.page_source)
        except:
            fakespot_grade = "0"
            print("error: " + amazon_url)
    driver.quit()
    return fakespot_grade

big["fs_grade"] = big["product_id"].map(lambda a: run_fakespot(a))
big.to_csv(f"../popular_graded_{timestamp}.csv", index=False)
