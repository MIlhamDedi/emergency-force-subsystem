# import uuid
import psycopg2
from .data_model import Asset, Plan, Report
conn = None
cursor = None


def connect(hostname, port, db_name, uid, pwd):
    """connect to SQL-Server in URL"""
    global conn
    global cursor
    url = "host=" + hostname + " port=" + port + " dbname="
    url += db_name + " user=" + uid + " password=" + pwd
    conn = psycopg2.connect(url)
    cursor = conn.cursor()


def get_plan():
    if conn is None:
        raise RuntimeError("connect to DB first by running connect(URL)")
    cursor.execute('select * from plan')
    plan_data = cursor.fetchall()
    plan_json = dict()
    for _ in range(len(plan_data)):
        plan_json[_] = Plan(plan_data[_][1], plan_data[_][2]).__dict__
    return plan_json


def get_report():
    if conn is None:
        raise RuntimeError("connect to DB first by running connect(URL)")
    cursor.execute('select * from report')
    report_data = cursor.fetchall()
    report_json = dict()
    for _ in range(len(report_data)):
        report_json[_] = Report(report_data[_][1], report_data[_][3]).__dict__
    return report_json


def get_asset():
    if conn is None:
        raise RuntimeError("connect to DB first by running connect(URL)")
    cursor.execute('select * from asset')
    asset_data = cursor.fetchall()
    asset_json = dict()
    for _ in range(len(asset_data)):
        asset_json[_] = Asset(asset_data[_][1], asset_data[_][2]).__dict__
    return asset_json
