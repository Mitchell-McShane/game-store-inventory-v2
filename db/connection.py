import os

import psycopg


def get_connection():
    return psycopg.connect(
        dbname="game_store_inventory",
        user="postgres",
        password=os.environ["GAME_STORE_DB_PASSWORD"],
        host="localhost",
        port=5432
    )
