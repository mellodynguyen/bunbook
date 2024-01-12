from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import os
import crud
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
        session["user_email"] = user.email
        # flash(f"Welcome back, {user.email}!")

        return redirect('/home')

@app.route('/home')
def timeline():
    """Display the timeline/feed"""

    return render_template('home.html')

# if user selects to add images, we'd need to commit the post and add the image
# to the post and change the route to the form to have it post it w/ image
# add a route for cloudinary: this route will show the form

# add a route for cloudinary: this route will process the form 
# this route should accept POST requests


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)