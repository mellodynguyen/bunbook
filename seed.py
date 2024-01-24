"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

# python will run dropdb and createdb for us using these commands
os.system('dropdb bunbook')
os.system('createdb bunbook')

# connect to the database and call db.create_all
model.connect_to_db(server.app)
server.app.app_context().push()
model.db.create_all()



# crud functions to create new user to make test users
# user1

# commit all users

# crud func to create post for each user
# add and commit posts to db - need posts in order for replies and likes


# crud func for reply
# add and commit reply

# crud func for post likes
# add and commit likes


# crud func for reply likes
# add and commit likes