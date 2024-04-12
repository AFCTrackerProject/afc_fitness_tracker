import os
from psycopg_pool import ConnectionPool

pool = None


def get_pool():
    global pool
    if pool is None:
        pool = ConnectionPool(
            conninfo='DB_CONNECTION_STRING'
        )
    return pool