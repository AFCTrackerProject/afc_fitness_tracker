import os
from psycopg_pool import ConnectionPool

pool = None

# This file establishes connection route to project database
def get_pool():
    global pool
    if pool is None:
        pool = ConnectionPool(
            conninfo=os.getenv('DB_CONNECTION_STRING')
        )
    return pool