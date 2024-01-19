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
    post_like = PostLike(user_id=user_id, post_id=post_id)
    
    return post_like

# def get_replies_by_postid(post_id):
#     """Get all replies for a specific Post."""
#     replies = Reply.query.filter(Reply.post_id == post_id).all()

#     return replies




# CRUD also needs to deal with database connections 
if __name__ == '__main__':
    from server import app
    connect_to_db(app)