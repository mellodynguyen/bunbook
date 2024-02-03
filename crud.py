"""CRUD operations."""

from model import db, User, Post, Images, PostLike, Reply, ReplyLike, Notification, connect_to_db

def create_user(email, password, screenname, birthday):
    """Create and return a new user."""

    user = User(email=email, password=password, screenname=screenname, birthday=birthday)

    return user

# to check if a user exists 
def get_user_by_email(email):
    return User.query.filter(User.email == email).first() 

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_post_id(post_id):
    return Post.query.get(post_id)

def get_user_by_reply_id(reply_id):
    return Reply.query.get(reply_id)

def create_post(user_id, body, timestamp, language):
    """Create a post and return the post"""
    post = Post(user_id=user_id, body=body, timestamp=timestamp, language=language)

    return post
    
def create_image(post_id, image_link):
    image = Images(post_id=post_id, image_link=image_link)
    
    return image 


def create_reply(user_id, post_id, body, timestamp):
    """Create a reply for a post and return the reply"""
    reply = Reply(user_id=user_id, post_id=post_id, body=body, timestamp=timestamp)

    return reply
    
# like is not a column so it is not a CRUD function we need to call out
def create_like_for_post(user_id, post_id):
    """Create a like for a post and return the like"""
    post_like = PostLike(user_id=user_id, post_id=post_id)
    
    return post_like

def create_user_pfp(user_id, image_link):
    """Create image for user profile picture"""
    current_user = get_user_by_id(user_id)
    current_user.profilepic = image_link
    
    return current_user

def create_user_header(user_id, image_link):
    """Create image for user profile picture"""
    current_user = get_user_by_id(user_id)
    
    current_user.headerpic = image_link
    
    return current_user

def create_user_info(user_id, screenname, bio, pronouns, location, birthday):
    current_user = get_user_by_id(user_id)
    current_user.screenname = screenname
    current_user.bio = bio
    current_user.pronouns = pronouns
    current_user.location = location
    current_user.birthday = birthday

    return current_user
def create_like_for_reply(user_id, reply_id):
    """Create a like for a reply and return the like"""

    reply_like = ReplyLike(user_id=user_id, reply_id=reply_id)

    return reply_like

def create_notification(user_id, notifier_id, post_id, type_of_thing, timestamp):
    """Create a notification"""

    notification = Notification(user_id=user_id, notifier_id=notifier_id, 
                                post_id=post_id, type_of_thing=type_of_thing,
                                timestamp=timestamp)
    
    return notification 
# CRUD also needs to deal with database connections 
if __name__ == '__main__':
    from server import app
    connect_to_db(app)