# create_database.py
from sqlalchemy_utils import database_exists, create_database


def create_postgresql_database(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
        print("Database created")
    print(database_exists(engine.url))
