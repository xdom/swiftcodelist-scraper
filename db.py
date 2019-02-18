import sqlite3
import sys


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return None


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def create_bic(conn, bic):
    sql = ''' INSERT INTO bic(swift,country,bank,branch,city,zipcode,address)
              VALUES(?,?,?,?,?,?,?) '''
    try:  
        cur = conn.cursor()
        cur.execute(sql, bic)
        return cur.lastrowid
    except sqlite3.Error as e:
        print(e)
