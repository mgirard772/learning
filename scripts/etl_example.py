"""
  usage: python etl_assignment [runs]

  The purpose of this assignment is to resolve a common ETL problem - namely duplicate & outdated data. For this assignment the
  pre-written generate_user_updates function will be returning data on 1 to 50 different users that have been updated 10 times. Your task 
  is to finish the functions remove_outdated_duplicates, update_sqlite_user_without_fetching and compare_final_user_rows_without_fetching which handle the 
  de-duping and the update of data in an SQL(ite) database (+ final compare of results). remove_outdated_duplicates should only return the most up-to-date user data 
  of each user decided by latest updatedAt timestamp. update_sqlite_user_without_fetching should only update users in the database if the 
  data is more up-to-date than what is already inserted. This code will loop several and the goal is for the final results in the 
  SQLite database to equal the contents of NEWEST_USER_DATA, which is the most up-to-date data between all of the loops.

  Some rules & clarifications:
    1) No priming the SQLite database with existing users (for final product)
    2) No saving “state” between loops (except for most up-to-date users in SQL users table as per assignment)
    3) No python libraries outside of standard
    4) No fetching data out of SQLite into python to manipulate
    5) Replace existing_user_data if existing_user_data.updated_at < new_user_data.updated_at
    6) “id” is the primary key
    7) Put your code where it says "YOUR CODE HERE" but feel free to add helper functions

  If anything is unclear or you have any questions feel free to email me at andrei@thoughtindustries.com - otherwise good luck!
"""


from sys import argv
from random import randint
from datetime import datetime
import sqlite3


# DO NOT EDIT OR USE THESE VARS IN FINAL PRODUCT
MAX_USERS = 50
JANUARY_FIRST_2020_TIMESTAMP_MS = 1577836800000
ONE_DAY_MS = 24 * 60 * 60 * 1000
NEWEST_USER_DATA = {}


def generate_user_updates(n_users=None, n_updates=10):
    """
      This function returns randomly generated user updates - your code will be tested with default parameter values
  
      DO NOT EDIT IN FINAL PRODUCT
    """
    n_users = randint(1, MAX_USERS) if n_users is None else n_users

    user_updates = []

    for i in range(0, n_users):
        for j in range(0, n_updates):
            user_updates.append({
                'id': i,
                'name': f'Joe {i}',
                'cookies': randint(1, 1000),
                'updated_at': JANUARY_FIRST_2020_TIMESTAMP_MS + j * ONE_DAY_MS + randint(0, 1000)
            })

    for user_update in user_updates:
        NEWEST_USER_DATA[user_update['id']] = user_update if user_update['id'] not in NEWEST_USER_DATA or NEWEST_USER_DATA[user_update['id']]['updated_at'] < user_update['updated_at'] else NEWEST_USER_DATA[user_update['id']]

    shuffled_user_updates = []
    while (len(user_updates)):
        user_update = user_updates.pop()
        random_index = randint(0, len(shuffled_user_updates))
        shuffled_user_updates.insert(random_index, user_update)

    return shuffled_user_updates


def remove_outdated_duplicates(updates):
    """
        remove duplicate updates per unique updates.id - most up-to-date update depends on updates.updated_at

        Args:
            updates (list[dict]): Dictionary of expected user rows (NEWEST_USER_DATA)

        Yields:
            dict[dict]:
                True/False indicating if rows in users table and expected_user_rows_match
    """
    deduped_updates = {}
    for update in updates:
        deduped_updates[update['id']] = update \
                if update['id'] not in deduped_updates or \
                   deduped_updates[update['id']]['updated_at'] < update['updated_at'] \
                else deduped_updates[update['id']]

    return deduped_updates


def update_sqlite_user_without_fetching(deduped_updates):
    """
        upsert deduped_updates into users table without fetching rows into python for manipulation (aka use SQL)

        Args:
            deduped_updates (dict): Dictionary of deduped updates to send to database

        Raises:
            Error: Raises an error if it fails to connect or send an update to the database
    """
    #Connect to SQLite
    try:
        conn = sqlite3.connect("temp.db")
    except:
        print("Couldn't connect to SQLite database")
        raise
    cur = conn.cursor()

    #Create users table if it doesn't exist
    create_users = ''' CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            cookies INTEGER,
                            updated_at INTEGER
                       ); '''
    try:
        cur.execute(create_users)
        conn.commit()
    except:
        print("Couldn't create users table")
        raise

    #Perform upserts
    upsert_user = ''' INSERT INTO users (id, name, cookies, updated_at) 
                      VALUES (?,?,?,?)
                      ON CONFLICT (id) DO 
                      UPDATE SET
                        cookies = ?,
                        updated_at = ?
                      WHERE updated_at < ?'''

    for update in deduped_updates.values():
        try:
            cur.execute(
                upsert_user,
                tuple(update.values()) + (update['cookies'], update['updated_at'], update['updated_at'])
            )
            conn.commit()
        except:
            print("Failed to upsert user")
            raise

    cur.close()
    conn.close()


def compare_final_user_rows_without_fetching(expected_user_rows):
    """
        compare sqlitedb users table rows to values in expected_user_rows by users.id without fetching into python for manipulation (aka use SQL)

        Args:
            expected_user_rows (dict): Dictionary of expected user rows (NEWEST_USER_DATA)

        Yields:
            boolean:
                True/False indicating if rows in users table and expected_user_rows_match

        Raises:
            Error: Raises an error if it fails to connect or send an update to the database
    """
    all_rows_match = False

    #Connect to SQLite
    try:
        conn = sqlite3.connect("temp.db")
    except:
        print("Couldn't connect to SQLite database")
        raise
    cur = conn.cursor()

    #Create expected_users table
    create_expected_users = ''' CREATE TABLE IF NOT EXISTS expected_users (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                cookies INTEGER,
                                updated_at INTEGER
                           ); '''

    try:
        cur.execute(create_expected_users)
        conn.commit()
    except:
        print("Couldn't create users table")
        raise

    #Insert expected user data
    insert_expected_user = ''' INSERT INTO expected_users (id, name, cookies, updated_at)
                               VALUES (?,?,?,?);'''

    for expected_user in expected_user_rows.values():
        try:
            cur.execute(
                insert_expected_user,
                tuple(expected_user.values())
            )
            conn.commit()
        except:
            print("Failed to insert expected_user")
            raise

    #Perform difference check against users and expected_users tables
    difference_check = ''' SELECT *, 'users' AS difference_location FROM users 
                           EXCEPT 
                           SELECT *, 'users' AS difference_location FROM expected_users
                           UNION ALL
                           SELECT *, 'expected_users' AS difference_location FROM expected_users 
                           EXCEPT 
                           SELECT *, 'expected_users' AS difference_location FROM users;
                           '''

    result = cur.execute(difference_check).fetchall()

    if result.__len__() == 0:
        all_rows_match = True

    #Clean-up
    cur.close()
    conn.close()

    import os
    os.remove("temp.db")

    return all_rows_match


def run_etl_sim(runs):
    """
      runs our little etl sim - feel free to edit for debugging but must remain unedited in final product
    """
    for _ in range(0, runs):
        updates = generate_user_updates(1,2)
        deduped_updates = remove_outdated_duplicates(updates)
        update_sqlite_user_without_fetching(deduped_updates)

    if compare_final_user_rows_without_fetching(NEWEST_USER_DATA):
        print("Success! User rows match expected values.")
    else:
        print("Failure! User rows do not match expected values.")

if __name__ == '__main__':
    runs = None
    try:
        runs = int(argv[1], 10)
    except:
        print("usage: python etl_example.py [runs]")
        raise
    run_etl_sim(runs)
