"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime
from passlib.hash import argon2

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

def create_user_for_seed(email,password,screenname,bio, pronouns, location, birthday):
    """Create and return a new user (seed file)."""

    user = model.User(email=email, password=password, screenname=screenname,
                      bio=bio, pronouns=pronouns, location=location, birthday=birthday)

    return user
# crud functions to create new user to make test users
users_data = [
    {"email": "mellody@test.com", "password": "oak123", "screenname": "babyoak",
     "bio": "", "pronouns": "She/her", "location": "Dallas, TX", "birthday": "1998-11-06"},
    {"email": "dubu@test.com", "password": "dubu123", "screenname": "dubu",
     "bio": "", "pronouns": "She/her", "location": "Dallas, TX", "birthday": "1995-01-22"},
    {"email": "pope@test.com", "password": "pope123", "screenname": "pope",
     "bio": "", "pronouns": "He/Him", "location": "Akron, OH", "birthday": "1996-04-26" },
    {"email": "alex@test.com", "password": "kayfalc123", "screenname": "kayfalc",
     "bio": "", "pronouns": "He/Him", "location": "St. Louis, MO", "birthday": "1992-05-10"},
    {"email": "kyle@test.com", "password": "klyde123", "screenname": "klyde",
     "bio": "", "pronouns": "He/Him", "location": "Ontario, CA", "birthday": "1998-11-06"},
    {"email": "kabocha@test.com", "password": "chibird123", "screenname": "HWLKabocha",
     "bio": "", "pronouns": "He/Him", "location": "Honolulu, HI", "birthday": "1990-12-19"},
    {"email": "muse@test.com", "password": "snsdfan123", "screenname": "muse",
     "bio": "", "pronouns": "They/Them", "location": "Romania", "birthday": "1994-11-10"},
    {"email": "etree@test.com", "password": "etree123", "screenname": "etree",
     "bio": "", "pronouns": "He/Him", "location": "Dallas, TX", "birthday": "1993-06-12"},
    {"email": "pianocellop@test.com", "password": "larry123", "screenname": "pianocellop",
     "bio": "", "pronouns": "He/Him", "location": "Dallas, TX", "birthday": "1995-08-11"},
    {"email": "jess@test.com", "password": "jess123", "screenname": "jessgonz",
     "bio": "", "pronouns": "She/her", "location": "Dallas, TX", "birthday": "1995-07-14"},
    {"email": "mochinica@test.com", "password": "monica123", "screenname": "mochinica",
     "bio": "", "pronouns": "She/her", "location": "Seattle, WA", "birthday": "1995-12-27"},
]

# commit all users, ** will unpack the values from the dictionary for named args
# for user_data in users_data:
#     user = create_user_for_seed(**user_data)
#     model.db.session.add(user)

for user_data in users_data:
    email = user_data["email"]
    password = user_data["password"]
    # Hash the password using argon2
    hashed_password = argon2.hash(password) 
    # Update the password in the user data
    user_data["password"] = hashed_password
    user = create_user_for_seed(**user_data)
    model.db.session.add(user)

model.db.session.commit()

model.db.session.commit()

user_ids = [user.user_id for user in model.User.query.all()]

# crud func to create post for each user
# user_id = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
for user_id in user_ids:
    post = crud.create_post(user_id=user_id, body="Test post", 
                            timestamp=datetime.now(), language="English")
    model.db.session.add(post)

model.db.session.commit()
# add and commit posts to db - need posts in order for replies and likes

mellodypfp = crud.create_user_pfp(1, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1706827621/zfclzlrqpwbsgwjvbtgk.jpg")
tinapfp = crud.create_user_pfp(2, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1707019775/Screenshot_20231221_115438_Discord_y6wmft.jpg")
popepfp = crud.create_user_pfp(3, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1706736581/IMG_0516_kxjg3d.jpg")
alexpfp = crud.create_user_pfp(4, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1706736581/falcon_noggwd.jpg")
kylepfp = crud.create_user_pfp(5, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1707019588/image_vtc0dz.png")
kabochapfp = crud.create_user_pfp(6, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1707019590/unknown_isv14w.png")
musepfp = crud.create_user_pfp(7, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1707019588/f1101192696_trjv4f.jpg")
etreepfp = crud.create_user_pfp(8, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1706829116/GEzAXsVbQAAxmTj_cxemmw.png")
larrypfp = crud.create_user_pfp(9, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1707031142/W2mRD_5c_veanhu.jpg")
jessicapfp = crud.create_user_pfp(10, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1707019718/418610701_687423846643440_7581254869379702743_n_qwvhd2.jpg")
monicapfp = crud.create_user_pfp(11, "https://res.cloudinary.com/dzvyvbnmf/image/upload/v1707022572/IMG_1205_ereuke.jpg")

model.db.session.add(mellodypfp, tinapfp)

model.db.session.add(popepfp, kabochapfp)
model.db.session.add(alexpfp, kylepfp)

model.db.session.add(musepfp, etreepfp)
model.db.session.add(jessicapfp, monicapfp)
model.db.session.add(larrypfp)

model.db.session.commit()

# crud func for reply, add and commit reply
replies_data = [
    {"user_id": 1, "post_id": 11, "body": "Test Reply 1", "timestamp": datetime.now()},
    {"user_id": 2, "post_id": 10, "body": "Test Reply 2", "timestamp": datetime.now()},
    {"user_id": 3, "post_id": 9, "body": "Test Reply 3", "timestamp": datetime.now()},
    {"user_id": 4, "post_id": 8, "body": "Test Reply 4", "timestamp": datetime.now()},
    {"user_id": 5, "post_id": 7, "body": "Test Reply 5", "timestamp": datetime.now()},
    {"user_id": 6, "post_id": 6, "body": "Test Reply 6", "timestamp": datetime.now()},
    {"user_id": 7, "post_id": 5, "body": "Test Reply 7", "timestamp": datetime.now()},
    {"user_id": 8, "post_id": 4, "body": "Test Reply 8", "timestamp": datetime.now()},
    {"user_id": 9, "post_id": 3, "body": "Test Reply 8", "timestamp": datetime.now()},
    {"user_id": 10, "post_id": 2, "body": "Test Reply 8", "timestamp": datetime.now()},
    {"user_id": 11, "post_id": 1, "body": "Test Reply 8", "timestamp": datetime.now()},
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
    {"user_id": 4, "post_id": 2},
    {"user_id": 5, "post_id": 2},
    {"user_id": 6, "post_id": 4},
    {"user_id": 7, "post_id": 3},
    {"user_id": 8, "post_id": 5},
    {"user_id": 9, "post_id": 6},
    {"user_id": 10, "post_id": 1},
    {"user_id": 11, "post_id": 8},
    {"user_id": 3, "post_id": 1},
    {"user_id": 8, "post_id": 1},
    {"user_id": 9, "post_id": 1},
    {"user_id": 7, "post_id": 1},
    {"user_id": 5, "post_id": 1},
    {"user_id": 3, "post_id": 1},
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
    {"user_id": 1, "reply_id": 2},
    {"user_id": 2, "reply_id": 3},
    {"user_id": 3, "reply_id": 4},
    {"user_id": 2, "reply_id": 5},
    {"user_id": 3, "reply_id": 6},
    {"user_id": 3, "reply_id": 7},
    {"user_id": 4, "reply_id": 8},
    {"user_id": 4, "reply_id": 9},
    {"user_id": 5, "reply_id": 10},
    {"user_id": 6, "reply_id": 11},
    {"user_id": 7, "reply_id": 8},
    {"user_id": 7, "reply_id": 1},
    {"user_id": 8, "reply_id": 1},
    {"user_id": 9, "reply_id": 1},
    {"user_id": 10, "reply_id": 1},
    {"user_id": 11, "reply_id": 1},
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

