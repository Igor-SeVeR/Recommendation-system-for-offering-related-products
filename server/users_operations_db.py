import json
import sys

from config import DATABASE
from passlib.context import CryptContext


def get_user(username: str):
    try:
        return DATABASE.get(username)
    except:
        print('Database is unable. Aborting...')
        exit(0)


def add_user(username: str, password: str, full_name: str, email: str):
    usr = get_user(username)

    # checking if username is already in database
    if usr:
        print('User named %s already exists. Aborting...' % username)
        exit(0)

    # hashing password
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    password = pwd_context.hash(password)

    # adding user to db
    user_dict = {'username': username, 'full_name': full_name,
                 'email': email, 'hashed_password': password, 'disabled': False}
    DATABASE.set(username, json.dumps(user_dict))
    print('Successfully added!')


def del_user(username: str):
    usr = get_user(username)
    if not usr:
        print('User named %s does not exist. Aborting...' % username)
        exit(0)
    DATABASE.delete(username)
    print('Successfully deleted!')


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[2] == 'delete_user':
        del_user(sys.argv[1])
    elif len(sys.argv) == 5:
        add_user(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print('Incorrect parameters number! Aborting...')
