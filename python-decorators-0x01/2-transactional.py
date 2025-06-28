import sqlite3 
import functools

def with_db_connection(func):
    def connect_db(*args, **kwargs):
      conn = sqlite3.connect('users.db')
      try:
        result =  func(conn, *args, **kwargs)
      finally:
         conn.close()
      return result
    return connect_db


def transactional(func):
    def transact_db(conn,*args, **kwargs):
      try:
        func(conn, *args, **kwargs)
        conn.commit()
      except sqlite3.Error as e:
         conn.rollback()

    return transact_db
  

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
  cursor = conn.cursor() 
  cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')