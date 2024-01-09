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
model.db.create_all()



