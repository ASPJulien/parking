import lastfmhandler
import json
from os.path import exists

users = {}

def read_db():
    if exists("users.json"):
        return json.loads(open("users.json").read())
    else:
        print("UsersDB does not exist, creating a new one to ./users.json.")
        with open("users.json", "w") as outfile:
            json.dump(users, outfile)
            return read_db()


def update_db():
    with open("users.json", "w") as outfile:
            json.dump(users, outfile)
    

def get_user(id):
    if str(id) in users:
        return users[str(id)]
    else:
        return "error"

def lastfm_user_exists(user):
    a = lastfmhandler.get_user_info(user)
    return 'error' not in a

def link_user(id, user):
    users[str(id)] = user
    update_db()
