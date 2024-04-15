from database.db import get_pool
from typing import Any
from psycopg.rows import dict_row


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
            conn.commit()  # Commit the INSERT operation

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
                print(f"Username '{username}' not found in the database.")
                raise Exception('User not found!')
            return user



