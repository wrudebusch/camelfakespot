import os

os.system("python3 popular_chrome.py")
os.system("python3 top_drops_chrome.py")

for name in ["top_drops", "popular"]:
    os.system(f"python3 any_csv_to_table.py {name}")
    os.remove(name + ".csv")
