from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Post, Reply
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


@app.route('/')
def homepage():
    """View homepage."""

    # this will show if the user is not logged in,
    # it should show create an account button that will route to /createaccount
    # or a log in button that routes the info to login and then redirect to /home

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
        # flash(f"Welcome back, {user.email}!")
        print("this is the session object")
        print(session)
        return redirect('/home')

@app.route('/home')
def timeline():
    """Display the timeline/feed"""
    # query database for all posts
    posts = Post.query.all()

    return render_template('home.html', posts=posts)



# if user selects to add images, we'd need to commit the post and add the image
# to the post and change the route to the form to have it post it w/ image
@app.route('/create-post', methods=["POST"])
def create_a_post():
    
    user_id = session["user_id"]

    body = request.form.get('post')

    timestamp = datetime.datetime.now()
    # format the date object with strftime() method
    # timestamp = currenttime.strftime('%m/%d/%y %H:%M')
    # print("this is the timestamp")
    # print(timestamp)
    # print(type(timestamp))
    
    # from CRUD.py: create_post(user_id, body, timestamp, language="english"):
    post = crud.create_post(user_id, body, timestamp, language="english")

    db.session.add(post)
    db.session.commit()

    return redirect('/home')

# add a route for cloudinary: this route will show the form


# add a route for cloudinary: this route will process the form 
# this route should accept POST requests


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)