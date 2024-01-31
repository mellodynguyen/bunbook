"""Models for BunBook"""

from flask_sqlalchemy import SQLAlchemy
import datetime

# give us a database (db) object 
db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    screenname = db.Column(db.String, nullable=False)
    # user profile photo
    profilepic = db.Column(db.String, default="")
    bio = db.Column(db.String, default="")
    pronouns = db.Column(db.String, default="")
    location = db.Column(db.String, default="")
    birthday = db.Column(db.Date, default="")

    # a user can have many posts
    user_posts = db.relationship("Post", back_populates="user")

    user_replies = db.relationship("Reply", back_populates="reply_user")

    user_notification = db.relationship("Notification", back_populates="user")
    
    # data model lecture example:
    # book = db.relationship("Book", back_populates="printings")
    # Class(Book) name and back_populates is how you relate the attributes in
    # the different classes to each other 

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
    # user_posts = db.relationship("Post", back_populates="user")

    # a post can have many replies
    reply = db.relationship("Reply", back_populates="reply_post")
    # reply_post = db.relationship("Post", back_populates="reply")

    # a post can have many likes
    like = db.relationship("PostLike", back_populates="postlikes")
    # postlikes = db.relationship("Post", back_populates="like")

    # multiple images to a post (one to many) but there will only be one post
    images = db.relationship("Images", back_populates="post")
    # post = db.relationship("Post", back_populates="images")

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

    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))

    postlikes = db.relationship("Post", back_populates="like")

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

    reply_post = db.relationship("Post", back_populates="reply")

    reply_user = db.relationship("User", back_populates="user_replies")

    def __repr__(self):
        return f'<Reply reply_id={self.reply_id} body_id={self.body}>'

class ReplyLike(db.Model):
    """Likes for a Reply"""

    __tablename__ = "replylikes"

    like_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    reply_id = db.Column(db.Integer, db.ForeignKey("replies.reply_id"))

    replylikes = db.relationship("Reply", back_populates="like")



    def __repr__(self):
        return f'<ReplyLike like_id{self.like_id}>'


class Notification(db.Model):
    """Notifications for User"""

    __tablename__ = "notifications"

    notification_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # Actor: who is the notification from
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    # who is the notification for
    notifier_id = db.Column(db.Integer, nullable=False)

    # what post is it for/against
    post_id = db.Column(db.Integer, nullable=False)

    # what type of thing did they interact with (str)
        # what is the id of the interaction (pairs with the type of thing)
            # when we run a query, we can have a conditional
    type_of_thing = db.Column(db.String)

    # when did it happen (timestamp)
    timestamp = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="user_notification")

    def __repr__(self):
        return f'<Notification notification_id{self.notification_id} from user_id{self.user_id}>'


# class NotificationObject(db.Model):
#     """Notifications for Posts"""

#     __tablename__ = "notificationobjects"

#     notificationobj_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     # what post is the notification for/against
#     post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"))
    
#     # what did they do the post? Like / Reply
    
#     # timestamp - so we can display how long ago was the notification
#     timestamp = db.Column(db.DateTime)



def connect_to_db(flask_app, db_uri="postgresql:///bunbook", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    app.app_context().push()
    db.create_all()