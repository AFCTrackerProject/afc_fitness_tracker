from database.db import get_pool
from typing import Any
from psycopg.rows import dict_row
from flask import flash, session

def get_all_workoutlogs():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                           SELECT workoutid, userid, WorkoutType, StartDateTime, EndDateTime
                           FROM workouthistory
                           """)
            return cursor.fetchall()

def insert_workout_log(userid, workoutid, workouttype, starttime, endtime):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            # Execute the SQL INSERT statement
            cursor.execute("""
                           INSERT INTO workouthistory (workoutid, userid, WorkoutType, StartDateTime, EndDateTime)
                           VALUES (%s, %s, %s, %s, %s)
                           """, (userid, workoutid, workouttype, starttime, endtime))
            # Commit the transaction
            conn.commit()
