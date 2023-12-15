# e2e: end-to-end encrypted instant messaging

## Mary Tsahas & Priya Naphade

e2e is an end-to-end encrypted messaging app developed as a final project for COS 316. 

### Instructions on how to run
1. Clone the github repository.
2. Ensure that all packages in requirements.txt are installed in your python environment.
3. Set an app key by setting an environemtal variable in terminal:
`export APP_SECRET_KEY = [some key]`
4. Start the server by running:
`python3 e2e.py`

### Using the webapp:
You can connect to the web app by navigating to the URL given in terminal where the server is running. 
***Note that you cannot have 2 accounts running on the same device.*** To test communication between clients, use different devices. 

To test the functionality, have 2 devices with different accounts logged into the home page. On one client, type the other client's username into the "Who do you want to chat with" form. Watch the client's connect and begin chatting instantaneously!