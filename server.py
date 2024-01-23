from flask import Flask, render_template, request, flash, session, redirect, jsonify, url_for
from model import connect_to_db, db, User, Post, Reply, PostLike, ReplyLike
import os
import crud
import datetime
# import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.secret_key = 'RANDOM SECRET KEY'

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dzvyvbnmf"

# helper function to calculate the length of likes for a post or reply instead 
# of storing count in database or a variable 
def calculatelikes(lst):
    """Calculate number of likes for a Post or Reply."""

    return len(lst)


# this will show if the user is not logged in,
# it should show create an account button that will route to /createaccount
# and log in button that routes the info to login and then redirect to /home
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/createaccount', methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    screenname = request.form.get("screenname")

    user = crud.get_user_by_email(email)
    if user:
        flash("An account with that email already exists.")
    else:
        user = crud.create_user(email, password, screenname)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")

        return redirect('/home')

# we'll need a button on the timeline page that routes to /logout
@app.route('/login', methods=["POST"])
def process_login():
    """Process user log in."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/')
    else:
        # Log in user by storing the user's email in session
        session["user_id"] = user.user_id
        session["screenname"] = user.screenname

        # flash(f"Welcome back, {user.email}!")
        # print("this is the session object")
        # print(session)
        return redirect('/home')

# need log out function!
#   session.pop('user_id', None)
#   session.pop('screenname', None)
    
@app.route('/logout')
def process_logout():
    """Process user log out"""
    
    session.pop('user_id', None)
    session.pop('screenname', None)
    
    flash("Logged out!")

    return redirect('/')


@app.route('/home')
def timeline():
    """View the timeline/feed"""
    # query database for all posts

    posts = Post.query.all()

    # query all the replies for a specific post 
    replies = Reply.query.all()

    # query all likes for posts
    # postlikes = Post.
    
    return render_template('home.html', posts=posts, replies=replies, 
                           calculatelikes=calculatelikes)


@app.route('/profile')
def profile():
    """View the User's profile"""

    # profile page should show the user's posts and replies
    user = crud.get_user_by_id(session['user_id'])
    # should also show their likes

    # add a form so the user can upload a photo that will be their pfp

   
    
    return render_template('profile.html', user=user, calculatelikes=calculatelikes)


# if user selects to add images, we'd need to commit the post and add the image
# to the post and change the route to the form to have it post it w/ image
@app.route('/create-post', methods=["POST"])
def create_a_post():
    """Process form to create a post and add it to the DB"""
    
    user_id = session["user_id"]

    body = request.form.get('post')
    
    timestamp = datetime.datetime.now()
    # format the date object with strftime() method
    # timestamp = currenttime.strftime('%m/%d/%y %H:%M')
    
    # from CRUD.py: create_post(user_id, body, timestamp, language="english"):
    post = crud.create_post(user_id, body, timestamp, language="english")

    db.session.add(post)
    db.session.commit()

    # if the user uploaded a file for their post, upload img to cloudinary
    # and add it to the database 
    user_file = request.files.get('my-file')
    if user_file: 
        img_url = upload_to_cloudinary(user_file)
        image = crud.create_image(post.post_id, img_url)

        db.session.add(image)
        db.session.commit()


    return redirect('/home')



@app.route('/create-reply', methods=["POST"])
def create_a_reply():
    """Process form to create a reply to a POST and add it to the DB"""
    
    user_id = session["user_id"]
    # print(user_id)
    post_id = int(request.form.get('post_id'))
    # print(post_id)
    # print(type(post_id))
    body = request.form.get('reply')
    # print(body)
    timestamp = datetime.datetime.now()
    # print(timestamp)

    reply = crud.create_reply(user_id, post_id, body, timestamp)

    db.session.add(reply)
    db.session.commit()


    return redirect('/home')



@app.route('/like-post', methods=['POST'])
def like_a_post():
    """Process liking a post."""

    # like_id = request.form.get('likebutton')

    user_id = session['user_id']
    post_id = int(request.form.get('likepostid'))
    # print(post_id)
    # print(type(post_id))
    postlike = crud.create_like_for_post(user_id, post_id)

    db.session.add(postlike)
    db.session.commit()

    return redirect('/home')

@app.route('/like-reply', methods=['POST'])
def like_a_reply():
    """Process liking a reply."""

    user_id = session['user_id']

    reply_id = int(request.form.get('likereplyid'))

    replylike = crud.create_like_for_reply(user_id, reply_id)

    db.session.add(replylike)
    db.session.commit()

    return redirect('/home')


# helper function to upload image to cloudinary
    
def upload_to_cloudinary(media_file):
    """Upload media file to Cloudinary"""
    result = cloudinary.uploader.upload(media_file, 
                                        api_key=CLOUDINARY_KEY, 
                                        api_secret=CLOUDINARY_SECRET, 
                                        cloud_name=CLOUD_NAME)
    return result['secure_url']




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)