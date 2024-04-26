from database.db import get_pool
from typing import Any
from psycopg.rows import dict_row
from flask import flash


def does_username_exist(username: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT 
                            userid
                        FROM
                            user
                        WHERE username = %s
                        """, [username])
            user_id = cur.fetchone()
            return user_id is not None
        
def create_user(firstname: str, lastname: str, email: str, username: str, password: str) -> dict:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (firstname, lastname, email, username, password)
                VALUES (%s, %s, %s, %s, %s)
            """, (firstname, lastname, email, username, password))
            conn.commit()  

    # Optionally return user data or a success message
    return {
        'firstname': firstname,
        'lastname': lastname,
        'email': email,
        'username': username
    }

def get_user_by_username(username: str) -> dict[str, Any]:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                        SELECT 
                            userid,
                            username,
                            password
                        FROM
                            users
                        WHERE username = %s
                        """, [username])
            user = cur.fetchone()
            if user is None:
                return None  
            return user


def submit_question(username: str, weight: float, height: float, gender: str, dateofbirth: str) -> bool:
    pool = get_pool()
    try:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                # Use parameterized query with float value
                cur.execute("""
                    UPDATE users
                    SET weight = %s, height = %s, gender=%s, dateofbirth=%s
                    WHERE username = %s
                """, (weight, height, gender, dateofbirth, username))
                conn.commit()  # Commit th  e UPDATE operation

                # Check if any rows were affected (i.e., if user with specified username exists)
                return cur.rowcount > 0
    except Exception as e:
        print(f"Error updating weight for user '{username}': {e}")
        return False

def get_user_by_id(userid: int) -> dict[str, Any] | None:
    pool = get_pool()
    with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute("""
                            SELECT
                                firstname,
                                lastname,
                                userid,
                                username,
                                email,
                                dateofbirth,
                                gender,
                                height,
                                weight
                            FROM
                                users
                            WHERE userid = %s
                            """,[userid])
                user = cur.fetchone()
                return user

def update_user_profile(userid: int, email: str, dateofbirth: str, gender: str, height: int, weight: int, profilepicture: bytes) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE users
                    SET email = %s, dateofbirth = %s, gender = %s, height = %s, weight = %s, ProfilePicture = %s
                    WHERE userid = %s
                """, (email, dateofbirth, gender, height, weight, profilepicture, userid))
                conn.commit()   

                return cur.rowcount > 0  # Check if the update was successful
