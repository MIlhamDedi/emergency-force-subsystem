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

# BASE URL for the server
try:
    BASE_URL = os.environ['BASE_URL']
except KeyError:
    BASE_URL = 'http://localhost:5000'

CMO_URL = 'https://bigbigcmo.herokuapp.com/api/ef/'

# App secret key (random)
SECRET_KEY = str(uuid4())
