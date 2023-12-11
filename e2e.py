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
    html_code = flask.render_template('home.html', username=session["username"])
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
    password = data['password']

    # Get user's password as stored in db
    db_password = fetchPassword(username)

	# Check if there is a row with specified username in db
    if db_password == None:
        return "no account"

	# If a row exists, check if passwords match
    if password == db_password[0]:
        session["username"] = username
        return "success"

    return "incorrect credentials"


# Add a user's credentials to the db if the username isn't taken
@app.route('/addcredentials', methods=['POST'])
def addcredentials():
    data = flask.request.json
    username = data['username']
    username = username.lower()
    password = data['password']

    # Check if an account already exists with username
    db_password = fetchPassword(username)

    if db_password != None:
        return("already exists")

    # add credentials to DB
    addCredentials(username, password)

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

	# Sanity check
    printtables()

    return "success"



# ------------------- Backend Information Delivery -------------------

# Fetch the password for a given username
def fetchPassword(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute("SELECT password FROM login_info WHERE username=?", [username])
    password = result.fetchone()
    conn.close()

    return password


# Add credentials to db
def addCredentials(username, password):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute("INSERT INTO login_info (username, password) VALUES(?, ?)", [username, password])
    conn.commit()
    conn.close()

    return

# Add users to each other's friendship table
def addFriendship(username, friend):

    # Create friends table for each user if needed
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(f"CREATE TABLE IF NOT EXISTS {username}(friend TEXT)")
    conn.close()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(f"CREATE TABLE IF NOT EXISTS {friend}(friend TEXT)")
    conn.close()

    # Add each user to the other's friendship table
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(f"SELECT * FROM {username} WHERE friend=?", [friend])
    hasFriend = result.fetchone()
    conn.close()

    if (hasFriend == None):
        print("First time y'all are becoming friends!")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        result = cursor.execute(f"INSERT INTO {username} (friend) VALUES(?)", [friend])
        conn.commit()
        conn.close()
    else:
        print("Y'all are already friends!")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(f"SELECT * FROM {friend} WHERE friend=?", [username])
    hasFriend = result.fetchone()
    conn.close()

    if (hasFriend == None):
        print("First time y'all are becoming friends!")
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        result = cursor.execute(f"INSERT INTO {friend} (friend) VALUES(?)", [username])
        conn.commit()
        conn.close()
    else:
        print("Y'all are already friends!")

    return


# Create messages table for storing chats
def createMessagesTable(username, friend):
    names = [username, friend]
    names.sort()
    sortedNames = ''.join(names)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(f"CREATE TABLE IF NOT EXISTS {sortedNames}(timestamp INTEGER, author TEXT, message TEXT)")
    conn.close()

    return


# Display all the tables in the database
def printtables():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    conn.close()

    print("Tables:", tables)

    return


if __name__ == '__main__':
    app.run(debug=True, port=5002)