import os
import datetime

x = datetime.datetime.now()
today = str(x.strftime("%Y-%m-%d"))

table_list = ["fakespot_results","popular_and_topdrop","popular","top_drops"]

command_list = []

for table in table_list:
    c = f"\copy (SELECT * FROM {table}) TO '{table}.csv' CSV HEADER;"
    command_list.append(c)

my_str = f"mkdir data_{today} && cd data_{today} \n"

for command in command_list: 
    y = f"psql --dbname 'postgres://postgres:black653!@192.168.1.26:5432/postgres' --command '{command}' \n"
    my_str+=y

my_str+=f"tar -czvf data_{today}.tar.gz * && cp data_{today}.tar.gz /media/pi/5CEA-1796/"

os.system(my_str)