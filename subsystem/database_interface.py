# import uuid
import psycopg2
from .config import *
url = "host=" + HOSTNAME + " port=" + PORT + " dbname="
url += DB_NAME + " user=" + UID + " password=" + PWD
conn = psycopg2.connect(url)
cursor = conn.cursor()


def get_plan():
    if conn is None:
        raise RuntimeError("connect to DB first by running connect(URL)")
    cursor.execute('select * from plan')
    plan_data = cursor.fetchall()
    return plan_data


def get_report():
    if conn is None:
        raise RuntimeError("connect to DB first by running connect(URL)")
    cursor.execute('select * from report')
    report_data = cursor.fetchall()
    return report_data


def get_asset():
    if conn is None:
        raise RuntimeError("connect to DB first by running connect(URL)")
    cursor.execute('select * from asset')
    asset_data = cursor.fetchall()
    return asset_data


def set_plan():
    pass


def set_report():
    pass


def set_asset():
    pass
