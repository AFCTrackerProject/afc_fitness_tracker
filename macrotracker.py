from database.db import get_pool
from typing import Any
from psycopg.rows import dict_row
from flask import flash

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
def create_macros(name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type):
    try:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                               INSERT INTO macrotracker (name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type)
                               VALUES (%s, %s, %s, %s, %s, %s)
                               """, (name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed, meal_type))
                conn.commit()
        return True  # Return True if insertion was successful
    except Exception as e:
        print("Error:", e)
        return False  # Return False if there was an error

def get_macros_by_meal_type(meal_type):
    try:
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute("""
                               SELECT name, caloriesconsumed, proteinconsumed, carbsconsumed, fatsconsumed
                               FROM macrotracker
                               WHERE meal_type = %s
                               """, (meal_type,))
                data = cursor.fetchall()
        return data
    except Exception as e:
        print("Error:", e)
        return None

