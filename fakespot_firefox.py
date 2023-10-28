#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
from sqlalchemy import create_engine

## setting enviroment variables
from dotenv import load_dotenv
from pathlib import Path

env_path = Path("..") / "test.env"
load_dotenv(dotenv_path=env_path)

pg_pass = os.environ.get("PG_PASS")
pg_host = os.environ.get("PG_HOST")
pg_db = os.environ.get("PG_DB")
pg_port = os.environ.get("PG_PORT")
pg_user = os.environ.get("PG_USER")


timestamp = str(time.time()).split(".")[0]
# print(timestamp)


def get_grade(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    review_div = soup.find_all("div", {"class": "review-grade"})
    grade = str(review_div[0]).split("<p>")[1].split("</p>")[0]
    return grade


def run_fakespot(item_id):
    driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
    driver.get("https://www.fakespot.com/analyzer")
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    print(soup)
    #cookie_button = driver.find_element_by_id("CybotCookiebotDialogBodyButtonDecline")
    cookie_button = driver.find_element("id","CybotCookiebotDialogBodyButtonDecline")
    cookie_button.click()
    amazon_url = "https://www.amazon.com/dp/" + item_id
    #search_box = driver.find_element_by_id("url-input-home")
    search_box = driver.find_element("id","url-input-home")
    search_box.send_keys(amazon_url)
    #search_button = driver.find_element_by_name("button")
    search_button = driver.find_element("name", "button")
    time.sleep(3)
    search_button.click()
    time.sleep(9)
    try:
        fakespot_grade = get_grade(driver.page_source)
    except:
        try:
            time.sleep(9)
            fakespot_grade = get_grade(driver.page_source)
            print(fakespot_grade)
        except:
            fakespot_grade = "0"
            print("error: " + amazon_url)
    driver.quit()
    return fakespot_grade


sql = """SELECT DISTINCT td.product_id
FROM top_drops AS td
JOIN popular as pop ON pop.product_id = td.product_id
LEFT JOIN fakespot_results AS fs ON td.product_id = fs.product_id
WHERE fs_grade IS NULL;
"""

engine = create_engine(f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")
con = engine.connect()
df = pd.read_sql(sql, con)
if len(df) > 0:
    df["fs_grade"] = df["product_id"].map(lambda a: run_fakespot(a))
    df.to_sql(
        "fakespot_results",
        con,
        schema="public",
        if_exists="append",
        index=False,
        chunksize=100,
        method="multi",
    )
