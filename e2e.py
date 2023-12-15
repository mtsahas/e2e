#!/usr/bin/env python

# -------------------------------------------------------------------
# e2e.py
# Authors: Priya Naphade & Mary Tsahas
# -------------------------------------------------------------------

import os
import flask
from flask import session
from flask_sock import Sock
import json

# ------------------------ App setup --------------------------------
app = flask.Flask(__name__, template_folder='static/templates')
sock = Sock(app)
app.secret_key = os.environ['APP_SECRET_KEY']

# list of all users in our app
users = []

# Store socket : client mappings
sock_map = {}

# Store public keys : client mappings
idkey_map = {}
otkey_map = {}

# -------------------------------------------------------------------


# Handle incoming messages, send outgoing messages based on message type
@sock.route('/handle')
def handle(sock):

    # Current socket is the sender's socket
    sock_map[session["username"]] = sock

    while True:
        data = sock.receive()
        # Convert string into python dict
        json_data = json.loads(data)

        # Normal messaging after olm handshake
        if json_data["type"] == "message":
            receiver = json_data["to"].lower()
            sender = json_data["from"].lower()
            receiver_sock = sock_map[receiver]

            # Send message to desired receiver through their socket
            formatted_send = {"type":"message", "to": receiver, "from":sender, "message":json_data["msg"]}
            receiver_sock.send(json.dumps(formatted_send))

        # Sender asking for receiver's public keys
        elif json_data["type"] == "key_query":
            # Whose key info do we need?
            receiver = json_data["to"].lower()

            # Take and then remove last element of one time keys
            ot_key = otkey_map[receiver].pop()
            id_key = idkey_map[receiver]

            # Sending back key information to same socket
            formatted_send = {"type":"key_send", "id_key":id_key, "ot_key":ot_key}
            sock.send(json.dumps(formatted_send))

        # Sender invites receiver to chat with them
        elif json_data["type"] == "invite":
            receiver = json_data["to"].lower()
            sender = json_data["from"].lower()
            receiver_sock = sock_map[receiver]
            message = json_data["message"]

            # Send invite to desired receiver through their socket
            formatted_send = {"type":"invite", "sender":sender,"message":message}
            receiver_sock.send(json.dumps(formatted_send))


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


# Verify a given username exists
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


# Add a user's credentials to users list if the username isn't taken
@app.route('/addcredentials', methods=['POST'])
def addcredentials():
    try:
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

    except:
        return "error"

# Store Olm keys of current user when they create an account
@app.route('/receivekeys', methods=['POST'])
def receivekeys():

    try:
        data = flask.request.json
        username = session["username"]
        id_key = data['id_key']
        one_time_keys = data["one_time_keys"]

        idkey_map[username] = id_key
        otkey_map[username] = one_time_keys
        return "success"

    except:
        return "error"


# Check if a chat is possible with some user
@app.route("/checkfriend", methods=['POST'])
def checkfriend():
    username = session["username"]
    data = flask.request.json
    friend = data['friend']
    friend = friend.lower()

    # Don't allow users to chat with themselves
    if friend == username:
        return "self chat"

    # Check if an account already exists with username
    if friend in users:
        return "success"

    return "no account"


@app.errorhandler(404)
def notfound(e):
    html_code = flask.render_template('404.html')
    response = flask.make_response(html_code)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
