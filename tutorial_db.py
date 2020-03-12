import sqlite3
from sqlite3 import Error

# will be used to check if database exists already
import os


# db_file arg is the name of your db
def create_connection(db_file):
    conn = None
    try:
        # connect to the db
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        # handle error, print it
        print(e)
    # return conn so that we can use it in main
    return conn

# check if tables exist
def check_for_tables(conn):
    conn = sqlite3.connect(r'simpledb.db')
    cursor = conn.cursor()

    # run this query to check for tables
    check_tables_query = """SELECT name FROM sqlite_master WHERE type='table';"""
    cursor.execute(check_tables_query)

    # if there are tables in the db, quit
    if cursor.fetchone() != None:
        print("Tables already exist!")
        quit()
    # else, proceed to create tables
    else:
        print("Tables do not exist, creating them now!")
        cursor.close()


"""
To run queries, you need 3 things:
Connection: create_connection()
Cursor from the connection: create_table()
Pass statement to execute() method of Cursor object
"""
# Creates the cursor and executes the statement
def create_table(conn, create_table_sql):
    try:
        # create cursor
        c = conn.cursor()
        # execute cursor statement
        c.execute(create_table_sql)
    except Error as e:
        # print error otherwise
        print(e)


def main():
    try:
        # check if db exists already
        if not os.path.exists('simpledb.db'):
            # naming the db simpledb.db, saving it to conn to be used later
            conn = create_connection(r'simpledb.db')
            print("Database created!")
        else:
            conn = create_connection(r'simpledb.db')
            print("Database already exists! Checking tables...")
    finally:
        # check for tables here
        check_for_tables(conn)

        # create project table query
        project_table = """CREATE TABLE IF NOT EXISTS projects (
                id integer PRIMARY KEY,
                name text NOT NULL,
                begin_date text,
                end_date text
                );"""

        # create tasks table query
        tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                id integer PRIMARY KEY,
                name text NOT NULL,
                priority integer,
                status_id integer NOT NULL,
                project_id integer NOT NULL,
                begin_date text NOT NULL,
                end_date text NOT NULL,
                FOREIGN KEY (project_id) REFERENCES projects (id)
            );"""

        # create project table
        create_table(conn, project_table)
        print("Project table created!")

        # create tasks table
        create_table(conn, tasks_table)
        print("Tasks table created!")

        print("All queries executed successfuly!")


if __name__ == '__main__':
    main()


"""SQLITE COMMANDS
    .shell pwd - displays pwd
    .cd /directory - change directory into given directory
    .open dbname.db - opens the specified db file
    .tables - lists tables in the current db
    .exit - exits the shell
"""
