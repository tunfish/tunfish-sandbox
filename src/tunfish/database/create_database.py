# create_database.py
from sqlalchemy_utils import database_exists, create_database


def create_postgresql_database(engine):
    print(f"create_postgresql_database")
    print(f"ENGINE.URL: {engine.url}")
    #if not database_exists(engine.url):
    #    print(f"inside if")
    #    create_database(engine.url)
    #    print("Database created")
    #print(database_exists(engine.url))
