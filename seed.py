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
users_data = [
    {"email": "mellody@test.com", "password": "oak123", "screenname": "babyoak"},
    {"email": "dubu@test.com", "password": "dubu123", "screenname": "dubu"},
    {"email": "pope@test.com", "password": "pope123", "screenname": "pope"},
    {"email": "alex@test.com", "password": "kayfalc123", "screenname": "kayfalc"},
    {"email": "kyle@test.com", "password": "klyde123", "screenname": "klyde"},
    {"email": "kabocha@test.com", "password": "chibird123", "screenname": "HWLKabocha"},
    {"email": "muse@test.com", "password": "snsdfan123", "screenname": "muse"},
    {"email": "etree@test.com", "password": "etree123", "screenname": "etree"},
]

# commit all users, ** will unpack the values from the dictionary for named args
for user_data in users_data:
    user = crud.create_user(**user_data)
    model.db.session.add(user)

model.db.session.commit()

user_ids = [user.user_id for user in model.User.query.all()]

# crud func to create post for each user
# user_id = 1, 2, 3, 4, 5, 6, 7, 8,
for user_id in user_ids:
    post = crud.create_post(user_id=user_id, body="Test post", 
                            timestamp=datetime.now(), language="English")
    model.db.session.add(post)

model.db.session.commit()
# add and commit posts to db - need posts in order for replies and likes


# crud func for reply, add and commit reply
replies_data = [
    {"user_id": 1, "post_id": 1, "body": "Test Reply 1", "timestamp": datetime.now()},
    {"user_id": 2, "post_id": 2, "body": "Test Reply 2", "timestamp": datetime.now()},
    {"user_id": 3, "post_id": 4, "body": "Test Reply 3", "timestamp": datetime.now()},
    {"user_id": 4, "post_id": 3, "body": "Test Reply 4", "timestamp": datetime.now()},
    {"user_id": 5, "post_id": 5, "body": "Test Reply 5", "timestamp": datetime.now()},
    {"user_id": 6, "post_id": 6, "body": "Test Reply 6", "timestamp": datetime.now()},
    {"user_id": 7, "post_id": 6, "body": "Test Reply 7", "timestamp": datetime.now()},
    {"user_id": 8, "post_id": 1, "body": "Test Reply 8", "timestamp": datetime.now()},
]

# Create and commit replies using a loop just like user_ids
for reply_data in replies_data:
    reply = crud.create_reply(**reply_data)
    model.db.session.add(reply)

    # Create notification for the reply
    notification_data = {
        "user_id": reply_data["user_id"],
        "notifier_id": reply_data["user_id"], 
        "post_id": reply_data["post_id"],
        "type_of_thing": "reply",
        "timestamp": reply_data["timestamp"]
    }

    model.db.session.add(crud.create_notification(**notification_data))

model.db.session.commit()


# crud func for post likes add and commit likes
likes_data_for_posts = [
    {"user_id": 1, "post_id": 1},
    {"user_id": 2, "post_id": 1},
    {"user_id": 3, "post_id": 1},
    {"user_id": 2, "post_id": 2},
    {"user_id": 3, "post_id": 2},
    {"user_id": 3, "post_id": 4},
    {"user_id": 4, "post_id": 3},
    {"user_id": 4, "post_id": 5},
    {"user_id": 5, "post_id": 6},
    {"user_id": 6, "post_id": 1},
    {"user_id": 7, "post_id": 8},
    {"user_id": 7, "post_id": 1},
    {"user_id": 8, "post_id": 1},
]

for like_data in likes_data_for_posts:
    post_like = crud.create_like_for_post(**like_data)
    model.db.session.add(post_like)

    notifier_id = crud.get_user_by_post_id(like_data["post_id"]).user_id

    notification_data_for_post_likes = {
        "user_id": like_data["user_id"],
        "notifier_id": notifier_id, 
        "post_id": like_data["post_id"],
        "type_of_thing": "like",
        "timestamp": datetime.now()
    }

    model.db.session.add(crud.create_notification(**notification_data_for_post_likes))

model.db.session.commit()


# crud func for reply likes add and commit likes
likes_data_for_replies = [
    {"user_id": 1, "reply_id": 1},
    {"user_id": 2, "reply_id": 1},
    {"user_id": 3, "reply_id": 1},
    {"user_id": 2, "reply_id": 2},
    {"user_id": 3, "reply_id": 2},
    {"user_id": 3, "reply_id": 4},
    {"user_id": 4, "reply_id": 3},
    {"user_id": 4, "reply_id": 5},
    {"user_id": 5, "reply_id": 6},
    {"user_id": 6, "reply_id": 1},
    {"user_id": 7, "reply_id": 8},
    {"user_id": 7, "reply_id": 1},
    {"user_id": 8, "reply_id": 1},
]
    
for like_data in likes_data_for_replies:
    reply_like = crud.create_like_for_reply(**like_data)
    model.db.session.add(reply_like)

    notifier_id = crud.get_user_by_reply_id(like_data["reply_id"]).user_id

    notification_data_for_likes = {
        "user_id": like_data["user_id"],
        "notifier_id": notifier_id, 
        "post_id": like_data["reply_id"],
        "type_of_thing": "like",
        "timestamp": datetime.now()
    }

    model.db.session.add(crud.create_notification(**notification_data_for_likes))

model.db.session.commit()

