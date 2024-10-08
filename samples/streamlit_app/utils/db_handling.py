import streamlit as st
from sqlalchemy import text


def get_conn():
    return st.connection("local_db", type="sql")


def create_table():
    conn = get_conn()
    query = (
        "CREATE TABLE IF NOT EXISTS results "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT, finished_at TEXT, "
        "target TEXT, status TEXT, test_passed_rate TEXT);"
    )
    with conn.session as s:
        s.execute(text(query))
        s.commit()


def insert_result(created_at, finished_at, target, status, test_passed_rate):
    conn = get_conn()
    query = (
        'INSERT INTO results '
        '(created_at, finished_at, target, status, test_passed_rate) '
        'VALUES '
        f'("{created_at}", "{finished_at}", "{target}", "{status}", "{test_passed_rate}");'
    )
    with conn.session as s:
        s.execute(text(query))
        s.commit()


def get_results():
    conn = get_conn()
    return conn.query("SELECT * FROM results;")


def delete_results(test_id):
    conn = get_conn()
    with conn.session as s:
        s.execute(text(f"DELETE FROM results where id={test_id};"))
        s.commit()