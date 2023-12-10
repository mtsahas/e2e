#!/usr/bin/env python

#-------------------------------------------------------------------
# e2e.py
# Authors: Priya Naphade & Mary Tsahas
#-------------------------------------------------------------------

#import os
import flask
#import urllib
#import database
#import auth
# -------------------------------------------------------------------

app = flask.Flask(__name__, template_folder='static/templates')
#app.secret_key = os.environ['APP_SECRET_KEY']

# -------------------------------------------------------------------

login_info = {}

@app.route('/logoutapp', methods=['GET'])
def logoutapp():
    return
    #return auth.logoutapp()


@app.route('/logoutcas', methods=['GET'])
def logoutcas():
    return #auth.logoutcas()


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # username = 'lyoder'#auth.authenticate()
    # tags = database.get_tags()
    html_code = flask.render_template('index.html')
    response = flask.make_response(html_code)
    return response

@app.route('/login', methods=['POST'])
def login():
    data = flask.request.json
    username = data['username']
    username = username.lower()
    password = data['password']

    success = False

    # First check if username is a key in login_info
    print(login_info)
    if username in login_info:
        # If username exists, check if password matches
        success = (login_info[username] == password)

    if(success):
        return "success"
    
    return "error"

@app.route('/profile', methods=['GET'])
def profile():
    html_code = flask.render_template('profile.html', username="Mary")
    response = flask.make_response(html_code)
    return response


@app.route('/newaccount', methods=['GET'])
def newaccount():
    html_code = flask.render_template('newaccount.html', username="Mary")
    response = flask.make_response(html_code)
    return response


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
    try: 
        login_info[username]=password
    except: 
        print(login_info)
        return "error"
    
    print(login_info)
    return "success"    

if __name__ == '__main__':
    app.run(debug=True, port=5002)