#!/usr/bin/env python

#-------------------------------------------------------------------
# e2e.py
# Authors: Priya Naphade & Mary Tsahas
#-------------------------------------------------------------------

import os
import flask
import sqlite3
from flask import session
#import urllib
#import database
#import auth
# -------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='static/templates')
app.secret_key = os.environ['APP_SECRET_KEY']


# -------------------------------------------------------------------



login_info = {}
login_info["alice"]="alice"
login_info["bob"]="bob"

chats = {}


@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def login():
    # username = 'lyoder'#auth.authenticate()
    # tags = database.get_tags()
    html_code = flask.render_template('login.html')
    response = flask.make_response(html_code)
    return response

@app.route('/auth', methods=['POST'])
def auth():
    data = flask.request.json
    username = data['username']
    username = username.lower()
    password = data['password']

    success = False

    # First check if username is a key in login_info
    #print(login_info)


    if username not in login_info:
        print("hello")
        return "no account"

    if username in login_info:
        # If username exists, check if password matches
        if (login_info[username] == password):
            session["username"] = username
            return "success"

        return "incorrect credentials"

    return "error"

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

    if friend == username:
        return "self chat"

    if friend not in login_info:
        return "no account"


@app.route('/addcredentials', methods=['POST'])
def addcredentials():
    data = flask.request.json
    username = data['username']
    username = username.lower()
    password = data['password']

    if username in login_info:
        print("hello!!!!!")
        print(login_info)
        return("already exists")

    # add credentials to DB
    login_info[username]=password
    session["username"] = username
    '''
    try:
        login_info[username]=password
        session["username"] = username

    except:
        print("ran into an error")
        print(login_info)
        return "error"
        '''

    print(login_info)
    return "success"

if __name__ == '__main__':
    app.run(debug=True, port=5002)