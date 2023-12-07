import socket
import threading

import rsa

public_key, private_key = rsa.newkeys(1024)
public_partner = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # internet socket, tcp
server.bind(("10.8.84.2", 9999))
server.listen() 

# basically defining client as server lol
client, _ = server.accept() # only accepts one connection

client.send(public_key.save_pkcs1("PEM")) ## sending my public key to whoever is connecting w me
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024)) ## receiving partners public key

def sending_messages(client):
    while True:
        message = input("")
        client.send(rsa.encrypt(message.encode(), public_partner))
        print("You: "+message)

def receiving_messages(client):
    while True:
        print("Partner: " + rsa.decrypt(client.recv(1024),private_key).decode()) # receiving in bytes, decrypting w our private key

## always communicating as client, even tho one client is technically server
# but that is ok

# how would we do this if we divided client and server into 2 files?
threading.Thread(target=sending_messages,args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()