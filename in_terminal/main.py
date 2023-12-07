import socket
import threading

import rsa

# choice of one client and one host, can make it into 2 seperate files..? idk

public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input("Do u want to host (1) or connect (2)?")

if choice == "1":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # internet socket, tcp
    server.bind(("10.8.84.2", 9999))
    server.listen() 

    # basically defining client as server lol
    client, _ = server.accept() # only accepts one connection
    # send key and then receive
    client.send(public_key.save_pkcs1("PEM")) ## sending my public key to whoever is connecting w me
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024)) ## receiving partners public key
elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("10.8.84.2",9999)) ## host ip address
    # receive key and then send
    public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024)) ## receiving partners public key
    client.send(public_key.save_pkcs1("PEM")) ## sending my public key to whoever is connecting w me

else:
    exit()

# sending messages
def sending_messages(client):
    while True:
        message = input("")
        # client.send(message.encode())
        client.send(rsa.encrypt(message.encode(), public_partner))
        print("You: "+message)

def receiving_messages(client):
    while True:
        # print("Partner: " + client.recv(1024).decode()) # receiving in bytes, decrypting w our private key

        print("Partner: " + rsa.decrypt(client.recv(1024),private_key).decode()) # receiving in bytes, decrypting w our private key

## always communicating as client, even tho one client is technically server
# but that is ok

# how would we do this if we divided client and server into 2 files?
threading.Thread(target=sending_messages,args=(client,)).start()
threading.Thread(target=receiving_messages, args=(client,)).start()