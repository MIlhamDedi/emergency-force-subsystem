# import uuid
import psycopg2
import uuid
from subsystem.config import HOSTNAME, PORT, DB_NAME, UID, PWD
url = "host=" + HOSTNAME + " port=" + PORT + " dbname="
url += DB_NAME + " user=" + UID + " password=" + PWD
conn = psycopg2.connect(url)
cursor = conn.cursor()
url = "host=localhost port=5432 dbname=postgres user=gehan password="


def get_plan():
    cursor.execute('select * from plan')
    plan_data = cursor.fetchall()
    return plan_data


def get_report():
    cursor.execute('select * from report')
    report_data = cursor.fetchall()
    return report_data


def get_asset():
    cursor.execute('select * from asset')
    asset_data = cursor.fetchall()
    return asset_data


def get_users():
    cursor.execute('select * from account')
    user_data = cursor.fetchall()
    return user_data


def set_plan():
    pass


def set_report():
    pass


def set_asset():
    pass


def add_users(username, pwd_hash, user_type):
    token = str(uuid.uuid4())
    try:
        cursor.execute(f'''
INSERT INTO "public"."account"("username", "pwd_hash", "type", "api_token")
VALUES('{username}', '{pwd_hash}', '{user_type}', '{token}');
''')
        conn.commit()
        return 0
    except psycopg2.IntegrityError:
        return 1
