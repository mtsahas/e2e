#!/usr/bin/env python

#-------------------------------------------------------------------
# e2e.py
# Authors: Priya Naphade & Mary Tsahas
#-------------------------------------------------------------------

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


@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login():
    html_code = flask.render_template('login.html')
    response = flask.make_response(html_code)
    return response


@app.route('/auth', methods=['POST'])
def auth():
    data = flask.request.json
    username = data['username']
    username = username.lower()
    password = data['password']

    # Get user's password as stored in db
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute("SELECT password FROM login_info WHERE username=?", [username])
    db_password = result.fetchone()
    conn.close()

	# Check if there is a row with specified username in db
    if db_password == None:
        return "no account"

	# If a row exists, check if passwords match
    if password == db_password[0]:
        session["username"] = username
        return "success"

    return "incorrect credentials"


@app.route('/home', methods=['GET'])
def home():
    html_code = flask.render_template('home.html', username=session["username"])
    response = flask.make_response(html_code)
    return response


@app.route('/newaccount', methods=['GET'])
def newaccount():
    html_code = flask.render_template('newaccount.html')
    response = flask.make_response(html_code)
    return response


@app.route("/startchat", methods=['POST'])
def startchat():
    username = session["username"]
    data = flask.request.json
    friend = data['friend']
    friend = friend.lower()

    if friend == username:
        return "self chat"

    # Check if an account already exists with username
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM login_info WHERE username=?", [friend])
    db_password = result.fetchone()
    conn.close()

    if db_password == None:
        return "no account"

    return "success"


@app.route('/addcredentials', methods=['POST'])
def addcredentials():
    data = flask.request.json
    username = data['username']
    username = username.lower()
    password = data['password']

    # Check if an account already exists with username
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM login_info WHERE username=?", [username])
    db_password = result.fetchone()
    conn.close()

    if db_password != None:
        return("already exists")

    # add credentials to DB
    ##### todo: add exception handling in try-catch statement
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute("INSERT INTO login_info (username, password) VALUES(?, ?)", [username, password])
    conn.commit()
    conn.close()

    session["username"] = username

    return "success"

if __name__ == '__main__':
    app.run(debug=True, port=5002)