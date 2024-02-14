# Bunbook
Bunbook is a social media web app by Mellody Nguyen. This web app allows users to create posts and interact with other user's and their posts!
![Bunbook Logo](/static/images/Bun-large-logo-09.png)

Mellody has always used social media web apps such Tumblr and Twitter as creative outlet and was interested in what it took to create her own. She wanted to implement the features she enjoyed such as being able to create posts with
or without images, replying, and liking posts/replies. She also enjoyed the customization and blog-like feel to
Tumblr and wanted to allow the users to customize their profiles, and many more things such as viewing their notifications or checking out other user's profiles. 

## Technologies Used
* Python
* Javascript
* Flask
* PostgreSQL
* SQLAlchemy
* Jinja2
* AJAX/JSON
* Bootstrap
* Cloudinary API
* Passlib and Argon2

(Dependencies are in requirements.txt)

### How to Run Bunbook
* Set up and activate a python virtualenv, and install all the dependencies:
    * `pip install -r requirements.txt`
* Make sure you have PostgreSQL running. Create a new database in psql named bunbook:
    * `createdb bunbook`
    * `db.create_all()`
    * Alternatively, you can run the seed.py file but this does contain dummy data!
        * `python3 seed.py`
* Start up the Flask server:
    * `python3 server.py`
* Go to localhost:5000 to see the web app

![Bunbook Log In Page](/static/images/welcome%20to%20bunkbook.jpg)
### How to use Bunbook
You'll need to create an account, once you create your account you'll be directed to the homepage or the "timeline."
Here, you'll be able to create a post and see any other post in the database. 
**Heads up** For creating a post with an image - If you never worked with Cloudinary before, be wary of your virtual machine (VM) having a "stale time"
from your computer being asleep or hiberating. It will make cloudinary think your request is "stale" or in the past!

#### Likes and Replies
Posts a `like` button shaped as a heart and a `reply` form to allow users to like and/or reply to posts. Posts also have a `show replies` button to show or hide all the replies for that particular post.

![Bunbook Homepage](/static/images/bunbook%20homepage.jpg)

#### Notifications
Press the `notifications` button on the side bar to go to the notifications page. You'll be able to see all the notifications for a particular post or reply. The notificaiton has a hyper-link to the user's profile and the post/reply in question. 
![Bunbook Notifications](/static/images/notifications.jpg)

#### Profile
Press the `profile` button the side bar to navigate to your profile page. Here you can click the `camera button`
on the top left to change your header or cover picture. You can also click the `edit profile` button to change details such as your profile picture, pronouns, location, and bio. 
The tabs `posts`, `replies`, `likes` can change your profiles current feed to show all your posts, replies and likes.
*Viewing another user's profile will just show a "limited view"* - meaning you are unable to make any changes to their profile details (bio, profile picture, etc.)
![Bunbook Profile](/static/images/profile.jpg)

Once you are done having fun you can press the `logout` button on the side bar!
Before you leave, make sure you check out the cool easter egg I created using Bunbook's mascot.
*Hint: Hover over the mascot on the side bar :D*

![Bunbook Meet the Dev](/static/images/Meet%20The%20Dev.jpg)

## Author
Mellody Nguyen is a software engineer in Dallas, Texas. She is currently pursuing a bachelors in computer science and expects to graduate in 2026!