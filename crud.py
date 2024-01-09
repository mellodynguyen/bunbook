"""CRUD operations."""

from model import db, User, Post, Images, PostLike, Reply, ReplyLike, connect_to_db

def create_user(email, password, screenname):
    """Create and return a new user."""

    user = User(email=email, password=password, screenname=screenname)

    return user

# to check if a user exists 
def get_user_by_email(email):
    return User.query.filter(User.email == email).first() 

def create_post(user_id, body, timestamp, language):
    """Create a post and return the post"""
    post = Post(user_id, body, timestamp,language)

    return post
    
def create_image(post_id, image_link):
    image = Images(post_id, image_link)
    
    return image 


def create_reply(user_id, post_id, body, timestamp):
    """Create a reply for a post and return the reply"""
    reply = Reply(user_id, post_id, body, timestamp)

    return reply
    
# like is not a column so it is not a CRUD function we need to call out





# CRUD also needs to deal with database connections 
if __name__ == '__main__':
    from server import app
    connect_to_db(app)