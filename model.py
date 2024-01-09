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
    posts = db.relationship("Post", back_populates="user")


    # data model lecture example:
    # book = db.relationship("Book", back_populates="printings")
    # Model(Book) name and table name(Printings)?

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
class Post(db.Model):
    """A post."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # what if the body has a picture/video too?
    body = db.Column(db.String, nullable=False)
    hasimage = db.Column(db.Boolean, nullable=False)
    # DateTime format?
    timestamp = db.Column(db.DateTime)
    language = db.Column(db.String, default="english")

    # one user can have many posts
    user = db.relationship("User", back_populates="posts")

    # a post can have many replies
    reply = db.relationship("Reply", back_populates="replies")

    # a post can have many likes
    like = db.relationship("PostLike", back_populates="postlikes")

    def __repr__(self):
        return f'<Post post_id={self.post_id}>'

class Images(db.Model):
    """images for a Post"""

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_link = db.Column(db.String, nullable=False)

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
