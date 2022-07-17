import argparse
from models import User, Messages
from psycopg2.errors import UniqueViolation
from clcrypto import check_password
from psycopg2 import connect, OperationalError


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password min 8 char")
parser.add_argument("-t", "--to", help="USERNAME to SEND message")
parser.add_argument("-s", "--send", help="Message")
parser.add_argument("-l", "--list", help="list of messges")

args = parser.parse_args()

def print_user_messages(cur, user):
    messages = Messages.load_all_messages(cur, user.id)
    for message in messages:
        from_ = User.load_user_by_id(cur, message.from_id)
        print(20 * "-")
        print(f"from: {from_.username}")
        print(f"data: {message.creation_date}")
        print(message.text)
        print(20 * "-")



def send_mess(cursor, from_id, recipient_name, text):
    if len(text) > 255:
        print('To long message! MAx 255 char!')
    to = User.load_user_by_username(cursor, recipient_name)
    if to:
        message = Message(from_id, to.id, text=text)
        message.save_to_db(cursor)
        print("Message sent!")
    else:
        print('Recipient does not exist!')

if __name__ == '__main__':
    try:
        conn = connect(database='workshop', user='postgres', password='Poczta3241567', host='localhost')
        conn.autocommit = True
        cursor = conn.cursor()
        if args.username and args.password:
            user = User.load_user_by_username(cursor, args.username)
            if check_password(cursor, user.hashed_password):
                if args.list:
                    print_user_messages(cursor, user)
                elif args.to and args.send:
                    send_mess(cursor, user.id, args.to, args.send)
                else:
                    parser.print_help()
            else:
                print('Incorrect password!')
        else:
            print('No such username in database! Username and password needed!')
            parser.print_help()
        conn.close()
    except OperationalError as error:
        print('Something wrong with connection: ', error)


