
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import string
import pickle 
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np
from clas_new import prediction_result

badwords = []
for line in open("badwords.txt"):
    for word in line.split( ):
        badwords.append(word)

# print(msg)
def censor(text, word):
  
    # Break down sentence by ' ' spaces
    # and store each individual word in
    # a different list
    word_list = text.split()
  
    # A new string to store the result
    result = ''
  
    # Creating the censor which is an asterisks 
    # "*" text of the length of censor word
    stars = '*' * len(word)
  
    # count variable to 
    # access our word_list
    count = 0
  
    # Iterating through our list
    # of extracted words
    index = 0;
    for i in word_list:
  
        if i == word:
              
            # changing the censored word to 
            # created asterisks censor
            word_list[index] = stars
        index += 1
  
    # join the words
    result =' '.join(word_list)
  
    return result

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    # print(msg)
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        msgString = msg.decode('utf-8')
        print (msgString)
        print(str(msgString.split(" ")))
        print("clients",clients[client])
        bullying = False
        finalmsg=''
        for word in msgString.split(" "):
            if word:
                
                # Load the model
                Y_predict=prediction_result(msg)
                for word in msgString.split(" "):
                    if word in badwords:
                        finalmsg=censor(msgString,word)
                        msgString=finalmsg
                print(msgString)
                 
                #print(Y_predict)
                #print ("bullying")
                if Y_predict == True:
                    # broadcast(bytes(msg, "utf8"))
                     broadcast(bytes("%s, Stop bullying people and behave decently. If you do this again we will block you." % name, "utf8"))                                   
                bullying = True
                break
        if bullying == False:
            # api.update_status("\n Good job, you're not a bully! (I am a bot in testing, don't take this too seriously)", status.id)
            # broadcast(bytes(msg, "utf8"))
            print ("not bullying")
        if msg != bytes("{quit}", "utf8"):
            print("3333333333333333333333333333")
            senddata=''
            senddata=bytes(msgString, 'utf-8')
            broadcast(senddata, name+": ")
        else:
            print("444444444444444444444444")
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break





def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
# SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()