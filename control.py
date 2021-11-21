#!/usr/bin/env python
# coding: utf-8
import os
import time
import random

random.seed()

time.sleep(random.randrange(60))
os.system("python3 chrome_main.py popular")

time.sleep(random.randrange(60))
os.system("python3 chrome_main.py top_drops")

for name in ["top_drops", "popular"]:
    os.system(f"python3 any_csv_to_table.py {name}")

os.system("python3 fakespot_firefox.py")
