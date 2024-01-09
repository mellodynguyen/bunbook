from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import os
# import cloudinary
import cloudinary.uploader

app = Flask(__name__)

CLOUDINARY_KEY = os.environ['CLOUDINARY_KEY']
CLOUDINARY_SECRET = os.environ['CLOUDINARY_SECRET']
CLOUD_NAME = "dzvyvbnmf"






# add a route for cloudinary: this route will show the form

# add a route for cloudinary: this route will process the form 
# this route should accept POST requests

