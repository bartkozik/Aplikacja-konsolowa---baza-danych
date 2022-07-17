import argparse
from models import User, Messages
from psycopg2.errors import UniqueViolation
from clcrypto import check_password
from psycopg2 import connect, OperationalError


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password min 8 char")
parser.add_argument("-n", "--new_pass", help="new password min 8 char")
parser.add_argument("-l", "--list", help="list of users")
parser.add_argument("-d", "--delete", help="delete user")
parser.add_argument("-e", "--edit", help="edit user")

args = parser.parse_args()

def list_users(cursor):
    users = User.load_all_users(cursor)
    for user in users:
        print(user.username)

def create_user(cursor, username, password):
    if len(password) < 8:
        print('To short password. Must contain min. 8 char!!!')
    else:
        try:
            user = User(username=username, password=password)
            user.save_to_db(cursor)
            print('User created')
        except UniqueViolation as error:
            print('User with this username already exist!!!', error)

def delete_user(cursor, username, password):
    user = User.load_user_by_username(username, password)
    if not user:
        print('No such user in database!')
    elif check_password(password, user.hashed_password):
        user.delete(cursor)
        print("User deleted!")
    else:
        print('Password incorrect!')


def edit_user(cursor, username, password, new_pass):
    user = User.load_user_by_username(cursor, username)
    if not user:
        print('No such user in database!')
    elif check_password(password, user.hashed_password):
        if len(new_pass) < 8:
            print('New password is to short, min 8 char!')
        else:
            user.hashed_password = new_pass
            user.save_to_db(cursor)
            print('New password created!')
    else:
        print('Password incorrect!!!')

if __name__ == '__main__':
    try:
        conn = connect(database="workshop", user="postgres", password="Poczta3241567",host="localhost")
        conn.autocommit = True
        cursor = conn.cursor()
        if args.username and args.password and args.new_pass:
            edit_user(cursor, args.username, args.password, args.new_pass)
        elif args.username and args.password and args.delete:
            delete_user(cursor, args.username, args.password)
        elif args.username and args.password:
            create_user(cursor, args.username, args.password)
        elif args.list:
            list_users(cursor)
        else:
            parser.print_help()
        conn.close()
    except OperationalError as error:
        print('That shit is cray and something went wrong with connection: ', error)