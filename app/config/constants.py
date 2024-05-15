# todo: use env

import os


API_VERSION = os.environ.get("API_VERSION")
API_PREFIX = "/api/" + API_VERSION
DATABASE_USER = os.environ.get("DATABASE_USER")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_DBNAME = os.environ.get("DATABASE_DBNAME")
DATABASE_HOST = os.environ.get("DATABASE_HOST")
