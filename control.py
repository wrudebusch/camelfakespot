import os

## setting enviroment variables
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(".") / "test.env"
load_dotenv(dotenv_path=env_path)

pg_pass = os.environ.get("PG_PASS")
pg_host = os.environ.get("PG_HOST")
pg_db = os.environ.get("PG_DB")
pg_port = os.environ.get("PG_PORT")
pg_user = os.environ.get("PG_USER")

os.system("python3 popular_chrome.py")
os.system("python3 top_drops_chrome.py")

for name in ["top_drops", "popular"]:
    os.system(f"python3 any_csv_to_table.py {name}")
    os.remove(name + ".csv")

try:
    psql_str = f"psql --dbname 'postgres://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}' -f update_fs_grade.sql;"
    os.system(psql_str)
    # os.system("rm *.csv")
except:
    print("psql error")
