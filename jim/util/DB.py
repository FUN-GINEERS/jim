import psycopg2
import sqlite3

from jim import config

CONN = None


def connect():
    global CONN
    backend = config.config_get("db", "backend")
    host = config.config_get("db", "host")
    name = config.config_get("db", "name")
    username = config.config_get("db", "username")
    passwd = config.config_get("db", "password")

    if CONN is None:
        if backend == "postgres":
            dsn = "dbname='%s' user='%s' host='%s' password='%s'" % (name, username, host, passwd,)
            CONN = psycopg2.connect(dsn)
        elif backend == "sqlite":
            CONN = sqlite3.connect(name)
        else:
            print("Database backend %s is not supported!" % (backend,))
            exit(0)


def query(q):
    connect()
    cur = CONN.cursor()
    cur.execute(q)
    return cur.fetchall()
