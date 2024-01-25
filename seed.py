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
testuser1 = crud.create_user("mellody@test.com", "babyoak", "oak123")
testuser2 = crud.create_user("dubu@test.com", "dubu", "dubu123")
testuser3 = crud.create_user("pope@test.com", "pope", "pope123")

# commit all users
model.db.session.add(testuser1, testuser2, testuser3)
model.db.session.commit()

# crud func to create post for each user
testpost1 = crud.create_post()
testpost2 = crud.create_post()
# add and commit posts to db - need posts in order for replies and likes


# crud func for reply
# add and commit reply

# crud func for post likes
# add and commit likes


# crud func for reply likes
# add and commit likes