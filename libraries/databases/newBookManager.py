#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml

from datetime import date
from libraries.databases.newBookModel import Almanewbooks
from libraries.utils import Logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

database = config['database']

# Create the engine and session
# Create the table
# Base.metadata.create_all(engine)


def connect():
    print("connecting...")
    engine = create_engine(f"mysql+pymysql://{database['user']}:{database['pass']}@{database['host']}:{database['port']}/{database['database']}?charset={database['charset']}", pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()


    alma_db_session = session        
    results = alma_db_session.query(Almanewbooks).all()

    print(len(results))
    alma_db_session.close()

def addBooksToAlmaDB():
    engine = create_engine(f"mysql+pymysql://{database['user']}:{database['pass']}@{database['host']}:{database['port']}/{database['database']}?charset={database['charset']}", pool_pre_ping=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_book = Almanewbooks(
        author='John Doe',
        ddc='372.7',
        isbn='9780123456789',
        released='2023',
        title='Example Book',
        date_added=date.today()
    )

    session.add(new_book)
    session.commit()
    session.close()

    connect()

if __name__ == "__main__":
    pass