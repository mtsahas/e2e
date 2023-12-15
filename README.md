# e2e: end-to-end encrypted instant messaging

## Mary Tsahas & Priya Naphade

e2e is an end-to-end encrypted messaging app developed as a final project for COS 316. 

### Instructions on how to run
1. Clone this GitHub repository.
2. Ensure that all packages in requirements.txt are installed in your python environment.
3. Set an app key by setting an environment variable in terminal:
`export APP_SECRET_KEY=[some key]`
4. Start the server by running:
`python3 e2e.py`

### Using the webapp
You can connect to the web app by navigating to the URL given in terminal where the server is running. 
***Note that you cannot have 2 accounts running on the same device.*** To test functionality, use 2 devices and create different e2e accounts on each device. Once both devices are logged in, type the client's username into the "Who do you want to chat with?" form. Watch the clients connect and begin chatting instantaneously 🥰

### Acknowledgements
Thank you to Mike for suggesting this as a project idea!
Thank you to Leon for helping us with Olm and our system design!