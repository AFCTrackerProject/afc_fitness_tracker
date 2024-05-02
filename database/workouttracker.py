from database.db import get_pool
from typing import Any
from psycopg.rows import dict_row
from flask import flash, session
from psycopg.rows import dict_row


def get_workout_logs(pool):
    with pool.connection() as conn:
        conn.row_factory = dict_row  # Set row factory to return rows as dictionaries
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT * FROM WorkoutHistory
                        """)
            workout_logs = cur.fetchall()
    return workout_logs


    

def insert_workout_log(userid, starttime, endtime, exercisename):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                   INSERT INTO WorkoutHistory (userid, exercisename, StartDateTime, EndDateTime)
                   VALUES (%s, %s, %s, %s)
                   """, (userid, exercisename, starttime, endtime))  # Ensure exercisename is in the correct position
    # Commit the transaction
    conn.commit()


