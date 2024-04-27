from database.db import get_pool
from typing import Any
from psycopg.rows import dict_row
from flask import flash, session

# Retrieves all macro entries from user in session
def get_all_macros():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                           SELECT name, logtime, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type
                           FROM macrotracker
                           """)
            return cursor.fetchall()

# Creates a macro entry from user in session 
def create_macros(userid, name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type):
    try:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                               INSERT INTO macrotracker (userid, name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type)
                               VALUES (%s, %s, %s, %s, %s, %s, %s)
                               """, (userid, name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type))
                conn.commit()
        return True  # Return True if insertion was successful
    except Exception as e:
        print("Error:", e)
        return False  # Return False if there was an error

def get_macros_by_meal_type(meal_type):
    try:
        pool = get_pool()
        UserID = session['userid']
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                               SELECT name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed
                               FROM macrotracker
                               WHERE meal_type = %s AND UserID = %s
                               """, (meal_type, UserID))
                data = cursor.fetchall()
        return data
    except Exception as e:
        print("Error:", e)
        return None

# User enters their target macros to get stored in DB
def save_target(userid: int, target_caloriesconsumed: float, target_proteinconsumed: float, target_carbsconsumed: float, target_fatsconsumed: float) -> bool:
    pool = get_pool()  # Call the function to get the pool object
    with pool.connection() as conn:  # Use the pool object to get a connection
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                        UPDATE macrotracker
                        SET target_caloriesconsumed = %s, target_proteinconsumed = %s, target_carbsconsumed = %s, target_fatsconsumed = %s
                        WHERE userid = %s
                        """, (target_caloriesconsumed, target_proteinconsumed, target_carbsconsumed, target_fatsconsumed, userid))
            conn.commit()
            return cur.rowcount > 0
