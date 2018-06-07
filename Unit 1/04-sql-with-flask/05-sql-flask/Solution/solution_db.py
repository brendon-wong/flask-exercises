import psycopg2
import psycopg2.extras


def connect():
    # Set db to flask-sql-snacks for general use, flask-sql-snacks-test for testng
    conn = psycopg2.connect("dbname=flask-sql-snacks-test")
    return conn


def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS snacks (id serial PRIMARY KEY, name text, kind text);")
    conn.commit()
    connect().close()


def close():
    connect().close()


# CRUD functions


def find_all_snacks():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM snacks;")
    close()
    return cur.fetchall()


def create_snack(name, kind):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO snacks (name, kind) VALUES (%s, %s);", (name, kind))
    conn.commit()
    close()


def find_snack(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM snacks WHERE id = %s;", (id,))
    close()
    return cur.fetchone()


def edit_snack(name, kind, id):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "UPDATE snacks SET name = %s, kind = %s WHERE id = %s;", (name, kind, id))
    conn.commit()
    close()


def remove_snack(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM snacks WHERE id = %s;", (id,))
    conn.commit()
    close()


# Reset the database
def reset_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("DROP SCHEMA public CASCADE;")
    cur.execute("CREATE SCHEMA public;")
    conn.commit()
    close()
