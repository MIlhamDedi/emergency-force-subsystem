import os
from uuid import uuid4
# Postgres Database Data
try:
    POSTGRES_URI = os.environ['DATABASE_URL']
except KeyError:
    POSTGRES_URI = None
# POSTGRES URI can be of two format:
# 1. "host=HOSTNAME port=PORT dbname=DB_NAME user=UID password=PWD"
# 2. postgres://UID:PWD@HOSTNAME:PORT/DB_NAME

# App secret key (random)
SECRET_KEY = str(uuid4())
