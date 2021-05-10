#!/usr/bin/env python
# coding: utf-8

import sys
import os
import logging
from datetime import datetime
import pandas as pd
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

name = sys.argv[1].strip().lower()

df = pd.read_csv(name + ".csv", low_memory=False)

if len(df) > 0:
    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )
    con = engine.connect()
    df.to_sql(
        name,
        con,
        schema="public",
        if_exists="append",
        index=False,
        chunksize=100,
        method="multi",
    )
    print(name + " done " + str(len(df)))
