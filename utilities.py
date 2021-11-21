import hashlib
import logging
from pathlib import Path


def get_logging(filename):
    """
    :return: the stdlib logging module configured with niceties
    """
    logging.basicConfig(
        level=logging.INFO,
        filename=Path(".") / f"{filename}.log",
        filemode="a",
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return logging


def hash_sha256(my_string: str):
    hash_object = hashlib.sha256(my_string.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


def fix_df(df):
    df = df.rename(str.lower, axis="columns")
    df.columns = df.columns.str.replace("[^a-zA-z0-9_]", "", regex=True)
    return df
