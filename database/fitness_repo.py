from database.db import get_pool
from typing import Any
from psycopg.rows import dict_row
from flask import flash
import secrets
import string

def generate_confirmation_token():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

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
        
def create_user(firstname: str, lastname: str, email: str, username: str, password: str, confirmation_token: str) -> dict:
    pool = get_pool()
    confirmation_token = generate_confirmation_token()  # Generate confirmation token
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (firstname, lastname, email, username, password, confirmation_token)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (firstname, lastname, email, username, password, confirmation_token))  # Include confirmation_token in the INSERT statement
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
                    weight,
                    profilepicture,
                    confirmation_token
                FROM
                    users
                WHERE userid = %s
            """, [userid])
            user = cur.fetchone()
            return user


def update_user_profile(userid: int, email: str, dateofbirth: str, gender: str, height: int, weight: int, profilepicture: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE users
                    SET email = %s, dateofbirth = %s, gender = %s, height = %s, weight = %s, profilepicture = %s
                    WHERE userid = %s
                """, (email, dateofbirth, gender, height, weight, profilepicture, userid))
                conn.commit()
                return cur.rowcount > 0  # Check if the update was successful
            except Exception as e:
                print(f"Error updating user profile: {e}")
                return False

def verify_confirmation_token(email: str, token_entered: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT confirmation_token
                FROM users
                WHERE email = %s
            """, [email])
            result = cur.fetchone()
            if result and result[0] == token_entered:
                return True
            else:
                return False
            
def get_confirmation_token(email: str) -> str:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT confirmation_token
                FROM users
                WHERE email = %s
            """, [email])
            result = cur.fetchone()
            if result:
                return result[0]  # Return the confirmation token
            else:
                return None  # If no confirmation token found for the email

