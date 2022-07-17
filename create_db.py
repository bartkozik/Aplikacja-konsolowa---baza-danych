from psycopg2 import connect, OperationalError
from psycopg2.errors import DuplicateDatabase, DuplicateTable

user = "postgres"
password = "Poczta3241567"
host = "localhost"

DB = "create database workshop;"

USERS = """create table users(
id serial primary key,
username varchar(255) unique,
hashed_password varchar(80));"""

MESSAGES = """create table messages(
id serial primary key,
from_id int references users(id) on delete cascade,
to_id int references users(id) on delete cascade,
text varchar(255),
creation_date timestamp default current_timestamp);"""


try:
    conn = connect(user=user, password=password, host=host)
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(DB)
        print('Database created!')
    except DuplicateDatabase as base_exists:
        print('Database exists!', base_exists)
    conn.close()
except OperationalError as errr:
    print('Operational ERROR - check it one more time!', errr)


try:
    conn= connect(database="workshop", user=user, password=password, host=host)
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(USERS)
        print('Table created!')
    except DuplicateTable as table_exists:
        print('Table exists!', table_exists)

    try:
        cursor.execute(MESSAGES)
        print('Table created!')
    except DuplicateTable as table_exists:
        print('Table exists!', table_exists)
    conn.close()

except OperationalError as errr:
    print('Operational ERROR - check it one more time!', errr)