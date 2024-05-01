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
                    confirmation_token,
                    confirmation_token_fp
                FROM
                    users
                WHERE userid = %s
            """, [userid])
            user = cur.fetchone()
            return user


def update_user_profile(userid: int, email: str, firstname: str, lastname: str, username: str, dateofbirth: str, gender: str, height: int, weight: int, profilepicture: str = None) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                if profilepicture:
                    cur.execute("""
                        UPDATE users
                        SET email = %s, firstname = %s, lastname = %s, username = %s, dateofbirth = %s, gender = %s, height = %s, weight = %s, profilepicture = %s
                        WHERE userid = %s
                    """, (email, firstname, lastname, username, dateofbirth, gender, height, weight, profilepicture, userid))
                else:
                    cur.execute("""
                        UPDATE users
                        SET email = %s, firstname = %s, lastname = %s, username = %s, dateofbirth = %s, gender = %s, height = %s, weight = %s
                        WHERE userid = %s
                    """, (email, firstname, lastname, username, dateofbirth, gender, height, weight, userid))
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
            
def update_confirmation_token(email: str, confirmation_token_fp: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE users
                    SET confirmation_token_fp = %s
                    WHERE email = %s
                """, (confirmation_token_fp, email))
                conn.commit()
                return cur.rowcount > 0  # Check if the update was successful
            except Exception as e:
                print(f"Error updating confirmation token: {e}")
                return False
            
def update_password(user_id: str, password: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    UPDATE users
                    SET password = %s
                    WHERE userid = %s
                """, (password, user_id))
                conn.commit()
                return cur.rowcount > 0  # Check if the update was successful
            except Exception as e:
                print(f"Error updating password: {e}")
                return False

def get_user_by_email(email: str) -> dict:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT
                    *
                FROM
                    users
                WHERE email = %s
            """, [email])
            user = cur.fetchone()
            return user

def get_user_by_confirmation_token(confirmation_token_fp: str) -> dict:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT *
                FROM users
                WHERE confirmation_token_fp = %s
            """, [confirmation_token_fp])
            user = cur.fetchone()
            return user
        
def verify_confirmation_token_fp(email: str, token_entered: str) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT confirmation_token_fp
                FROM users
                WHERE email = %s
            """, [email])
            result = cur.fetchone()
            if result and result[0] == token_entered:
                return True
            else:
                return False
            
    
def get_userid_by_email(email: str) -> dict:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT userid
                    FROM users
                    WHERE email = %s
                """, (email,))
                user_id = cur.fetchone()
                if user_id:
                    return user_id[0]  # Return the email string
                else:
                    return None
            except Exception as e:
                print(f"Error retrieving user id: {e}")
                return None
        
def get_useremail_by_tokenfp(confirmation_token_fp: str) -> str:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT email
                    FROM users
                    WHERE confirmation_token_fp = %s
                """, (confirmation_token_fp,))
                email = cur.fetchone()
                if email:
                    return email[0]  # Return the email string
                else:
                    return None
            except Exception as e:
                print(f"Error retrieving user email: {e}")
                return None
            
def is_username_available(username: str) -> bool:
    # Query the database to check if the username exists
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
            count = cur.fetchone()[0]
            return count == 0  # Return True if count is 0 (username is available), False otherwise

def is_email_available(email: str) -> bool:
    # Query the database to check if the email exists
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
            count = cur.fetchone()[0]
            return count == 0  # Return True if count is 0 (email is available), False otherwise

def remove_user_data(userid: int) -> bool:
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            try:
                # Delete user's data from all relevant tables
                cur.execute("""
                    DELETE FROM users
                    WHERE userid = %s
                """, (userid,))
                # You can add similar DELETE queries for other tables related to user data

                conn.commit()
                return True
            except Exception as e:
                print(f"Error removing user data: {e}")
                return False

