import psycopg2
import uuid
from subsystem.config import POSTGRES_URI
conn = psycopg2.connect(POSTGRES_URI)
cursor = conn.cursor()


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


def get_crisis():
    cursor.execute('select * from crisis')
    crisis_data = cursor.fetchall()
    return crisis_data


def get_users():
    cursor.execute('select * from account')
    user_data = cursor.fetchall()
    return user_data


def set_asset():
    pass


def add_plan(plan_id, crisis_id, details, time):
    try:
        cursor.execute(f'''
INSERT INTO "public"."plan"("id", "crisis_id", "details", "time")
VALUES('{plan_id}', '{crisis_id}', '{details}', '{time}')
''')
        conn.commit()
        return 0
    except psycopg2.DataError:
        return 1


def add_report(crisis_id, summary, time):
    try:
        cursor.execute(f'''
INSERT INTO "public"."report"("crisis_id","summary", "time")
VALUES('{crisis_id}', '{summary}', '{time}')
''')
        conn.commit()
        return 0
    except psycopg2.DataError:
        return 1


def add_crisis(crisis_id, crisis_type, description, time):
    try:
        cursor.execute(f'''
INSERT INTO "public"."plan"("id", "type", "description", "time")
VALUES('{crisis_id}', '{crisis_type}', '{description}', '{time}')
''')
        conn.commit()
        return 0
    except psycopg2.DataError:
        return 1


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
