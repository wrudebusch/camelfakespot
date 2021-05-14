#!/usr/bin/env python
# coding: utf-8
import os
import time
import random

random.seed()

time.sleep(random.randrange(60))
os.system("python3 popular_chrome.py")

time.sleep(random.randrange(60))
os.system("python3 topdrops_chrome.py")

for name in ["topdrops", "popular"]:
    os.system(f"python3 any_csv_to_table.py {name}")
    os.remove(name + ".csv")

os.system("python3 fakespot_firefox.py")