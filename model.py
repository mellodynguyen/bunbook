"""Models for BunBook"""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    screenname = db.Column(db.String, nullable=False)

    # a user can have many posts
    user_posts = db.relationship("Post", back_populates="user")


    # data model lecture example:
    # book = db.relationship("Book", back_populates="printings")

    # Class(Book) name and back_populates is how you relate the attributes in
    # the difference classes to each other 

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
class Post(db.Model):
    """A post."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # what if the body has a picture/video too?
    body = db.Column(db.String, nullable=False)

    # can get rid of hasimage because of the relationship (line 54)
    # hasimage = db.Column(db.Boolean, nullable=False)

    # DateTime format?
    timestamp = db.Column(db.DateTime)
    language = db.Column(db.String, default="english")

    # one user can have many posts
    user = db.relationship("User", back_populates="user_posts")

    # a post can have many replies
    reply = db.relationship("Reply", back_populates="replies")

    # a post can have many likes
    like = db.relationship("PostLike", back_populates="postlikes")

    # multiple images to a post (one to many) but there will only be one post
    images = db.relationship("Images", back_populates="post")

    # testing purposes:
    # post.images will be a list and will have an image objects, 
    # and if it doesnt, the list will be empty (no images)

    def __repr__(self):
        return f'<Post post_id={self.post_id}>'

class Images(db.Model):
    """images for a Post"""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))
    image_link = db.Column(db.String, nullable=False)

    post = db.relationship("Post", back_populates="images")

    def __repr__(self):
        return f'<Images image_id={self.image_id} image_link={self.image_link}>'





class PostLike(db.Model):
    """Likes for a Post"""

    __tablename__ = "postlikes"

    like_id = db.column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))

    def __repr__(self):
        return f'<Like like_id{self.like_id}>'

class Reply(db.Model):
    """Reply to a Post"""

    __tablename__ = "replies"
    
    reply_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))
    body = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime)
    # language = db.Column(db.String, default="english")

    # a reply can have many likes
    like = db.relationship("ReplyLike", back_populates="replylikes")

    def __repr__(self):
        return f'<Reply reply_id={self.reply_id}>'

class ReplyLike(db.Model):
    """Likes for a Reply"""

    __tablename__ = "replylikes"

    like_id = db.column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("replies.reply_id"))

    def __repr__(self):
        return f'<ReplyLike like_id{self.like_id}>'
