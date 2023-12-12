#!/usr/bin/env python

# -------------------------------------------------------------------
# e2e.py
# Authors: Priya Naphade & Mary Tsahas
# -------------------------------------------------------------------

import os
import flask
import sqlite3
from flask import session


# ------------------------ App setup --------------------------------
app = flask.Flask(__name__, template_folder='static/templates')
app.secret_key = os.environ['APP_SECRET_KEY']

# Initialize login_info table
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
result = cursor.execute("CREATE TABLE IF NOT EXISTS login_info(username TEXT, password TEXT)")
conn.close()
# -------------------------------------------------------------------

users = ["priya"]

# Display login page
@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login():
    html_code = flask.render_template('login.html')
    response = flask.make_response(html_code)
    return response


# Display home page
@app.route('/home', methods=['GET'])
def home():
    username = session["username"]

    html_code = flask.render_template('home.html', username=username)
    response = flask.make_response(html_code)
    return response


# Display new account page
@app.route('/newaccount', methods=['GET'])
def newaccount():
    html_code = flask.render_template('newaccount.html')
    response = flask.make_response(html_code)
    return response


# Verify a given username / password pair
@app.route('/auth', methods=['POST'])
def auth():
    data = flask.request.json
    username = data['username']
    username = username.lower()

    # Check if user account exists
    if (username in users):
        session["username"] = username
        return "success"

    return "no account"


# Add a user's credentials to the db if the username isn't taken
@app.route('/addcredentials', methods=['POST'])
def addcredentials():
    data = flask.request.json
    username = data['username']
    username = username.lower()

    # Check if an account already exists with username
    if (username in users):
        return("already exists")

    # add credentials to users list
    users.append(username)

    session["username"] = username

    return "success"


# Check if a chat is possible with some user
@app.route("/checkfriend", methods=['POST'])
def checkfriend():
    username = session["username"]
    data = flask.request.json
    friend = data['friend']
    friend = friend.lower()

    if friend == username:
        return "self chat"

    # Check if an account already exists with username
    db_password = fetchPassword(friend)

    if db_password == None:
        return "no account"

    return "success"


# Create a chat between two users: add each user's to the others' friends
# and create a messages table
@app.route("/createchat", methods=['POST'])
def createchat():

    username = session["username"]
    data = flask.request.json
    friend = data['friend']
    friend = friend.lower()

    # Add each user to the other's friendship table
    addFriendship(username, friend)

    # Create messsages table for storing chats
    createMessagesTable(username, friend)

    return "success"




if __name__ == '__main__':
    app.run(debug=True, port=5002)