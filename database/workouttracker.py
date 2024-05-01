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


    

def insert_workout_log(userid, ExerciseName, Equipment, TargetMuscle, Duration, StartDateTime, EndDateTime, pool):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                   INSERT INTO WorkoutHistory (userid, exercisename, Equipment, TargetMuscle, Duration, StartDateTime, EndDateTime)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)
                   """, (userid, ExerciseName, Equipment, TargetMuscle, Duration, StartDateTime, EndDateTime))
    # Commit the transaction
    conn.commit()

