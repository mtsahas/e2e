#!/usr/bin/env python

# -------------------------------------------------------------------
# e2e.py
# Authors: Priya Naphade & Mary Tsahas
# -------------------------------------------------------------------

import os
import flask
import sqlite3
from flask import session
from flask_sock import Sock
import asyncio
import websockets
import json

# ------------------------ App setup --------------------------------
app = flask.Flask(__name__, template_folder='static/templates')
sock = Sock(app)
app.secret_key = os.environ['APP_SECRET_KEY']

# Initialize login_info table
conn = sqlite3.connect("database.db")
cursor = conn.cursor()
result = cursor.execute("CREATE TABLE IF NOT EXISTS login_info(username TEXT, password TEXT)")
conn.close()
# -------------------------------------------------------------------

users = []
all_clients = []
buddies = []
sock_map = {}
idkey_map = {}
otkey_map = {}

'''
async def send_message(message):
    for client in all_clients:
        await client.send(message)

async def new_client_connected(client_socket, path):
    print("new client connected!")

    # add new socket to list of client sockts
    all_clients.append(client_socket)
    print(all_clients)

    while True:
       new_message = await client_socket.recv()
       print("Client sent:", new_message)
       await send_message(new_message)

async def start_server():
    print('server started!')
    await websockets.serve(new_client_connected, "localhost", 5003)
'''



# echo
@sock.route('/echo')
def echo(sock):
    sock_map[session["username"]] = sock
    
    print("Just gave", session["username"], "socket", sock)
    print("Echo sock:", sock)
    while True:
        data = sock.receive()
        print(data)
        # convert string into python dict
        json_data = json.loads(data)

        # normal messaging after olm handshake

        if json_data["type"] == "message":
            receiver = json_data["to"]
            receiver = receiver.lower()
            sender = json_data["from"]
            receiver_sock = sock_map[receiver]

            formatted_send = {"type":"message", "to": receiver, "from":sender, "message":json_data["msg"]}
            receiver_sock.send(json.dumps(formatted_send))
        elif json_data["type"] == "key_query":
            # whose key info do we need?
            receiver = json_data["to"].lower()
            # taking and removing last element of one time keys
            ot_key = otkey_map[receiver].pop()
            id_key = idkey_map[receiver]
            formatted_send = {"type":"key_send", "id_key":id_key, "ot_key":ot_key}
            sock.send(json.dumps(formatted_send)) ## sending back to same socket

        elif json_data["type"] == "invite":
            receiver = json_data["to"].lower()
            sender = json_data["from"]
            receiver_sock = sock_map[receiver]
            message = json_data["message"]

            formatted_send = {"type":"invite", "message":message}
            receiver_sock.send(json.dumps(formatted_send))
        
        ## what sock receives:
        # 1. regular message (message)
        # 2. request to talk to someone (key_query)
        # 3. first time message (invite)

        ## what we send through socks:
        # 1. public keys + ot key (key_send)
        # 2. invite (first message --> to create inbound on js) (first_message)
        # 3. regular messaging (message)

        print(sock_map)
        print("Echo sock:", sock)
       


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

@app.route('/receivekeys', methods=['POST'])
def receivekeys():
    data = flask.request.json
    username = session["username"]
    id_key = data['id_key']
    one_time_keys = data["one_time_keys"]
    try:
        idkey_map[username] = id_key
        otkey_map[username] = one_time_keys ## list of keys
        print("ID key map:", idkey_map)
        print("OT key map:", otkey_map)
    except:
        return "error"


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
    if friend in users:
        return "success"

    return "no account"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
