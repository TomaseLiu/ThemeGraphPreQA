#encoding=utf-8
import pymysql
import inspect
import sys
import os

SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))  
entity_module_dir = "entity"
sys.path.append(os.path.join(SCRIPT_DIR, entity_module_dir))


user_default = 'root'
passwd_default = '123456'
db_default = 'datayestsk'
host_default = 'localhost'
port_default = '3307'
charset_default = 'utf8'

"""
APIs for access to Database.
"""


def conn(user=user_default, passwd=passwd_default, db=db_default, host=host_default, charset=charset_default):
    """
    connect to database;
    default: local database;
    """
    conn = pymysql.connect(user=user, passwd=passwd, db=db, host=host, charset=charset)
    cursor = conn.cursor()
    return cursor, conn

def query(cursor, sql_str):
    """
    query data from database with sql statement;
    """
    cursor.execute(sql_str)
    return cursor

def insert(cursor, conn, sql_str):
    """
    insert data into database;
    """
    cursor.execute(sql_str)
    conn.commit()
    return cursor

def fetch_one_row(cursor):
    data = cursor.fetchone()
    if None == data:
        return None
    desc = cursor.description

    data_dict = {}
    for (key, value) in zip(desc, data):
        data_dict[key[0]] = value

    return data_dict

def close(cursor):
   cursor.close() 
    
