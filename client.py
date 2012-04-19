"""
Chat Client - RSA Assignment.
Beth Cooper
Shawn Zamechek
Qing Xie

Threaded Chat Client. There is a thread to read from the keyboard and
write to the socket and another thread to read from the socket and print to the screen.
The send thread sends the public key to the client while the recv thread receives the server's
public key and assigns the key to the global variable serverPublic. 
"""


import socket
from threading import Thread
import rsa
import sys, time
import bruteforce


READ_SIZE = 1024
BLOCK_SIZE = 10
HOST ="localhost"
PORT = 8888
serverPublic = [0 for x in range(2)]
RUNNING = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #global socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

"""
I do not the like passing one param with a comma separator, Seems confusing so wrote my own version of connect 
"""
def myconnect(host, port):
    s.connect((host, port))
    
"""
Called by the send thread. This function sends its own public key to the server. It then enters a loop to read from the keyboard and write to the socket. It encrypts the message using the server's public key.
"""
def send (s, keys):
    global RUNNING
    mykeys = str(keys[0]) + "," + str(keys[1])
    totalsent = 0
    while (totalsent < len(mykeys)):
        sent = s.send(mykeys[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
    print "Public key sent"
    time.sleep(.1)#sleep used to clean up printing errors due to thread order.
    print "Enter a Message"
    while RUNNING:
        message = raw_input("")
        totalsent = 0
        encryptedMessage = ''
        for c in message:
            encryptedChunk = str(rsa.encrypt(c, serverPublic))  
            neededZeros = BLOCK_SIZE - len(encryptedChunk)
            encryptedMessage += neededZeros * '0' + encryptedChunk
        while (totalsent < len(encryptedMessage)):
            sent = s.send(encryptedMessage[totalsent:])
            if sent == 0:
                raise RuntimeError("connection broken")
            totalsent = totalsent + sent
        if message == "quit":
            RUNNING = False
            break

"""
Called by the recv thread. This function receives the server's public key. It then enters a loop to read from the socket and write to the screen. It decrypts the message using its own public key.
"""
def recv(s, keys):
    global serverPublic
    global RUNNING
    temp = s.recv(READ_SIZE)
    tempPublic = temp.split(',')
    serverPublic[0] = int(tempPublic[0])
    serverPublic[1] = int(tempPublic[1])
    print "Public key Received"
    connDets = s.getpeername()
    remoteIP = connDets[0]
    remotePort = str(connDets[1])
    print  "connected to " + remoteIP + ":" + remotePort
    time.sleep(.1)#sleep used to clean up printing errors due to thread order.
    print "Sending the server's public"
    print serverPublic
    serverPrivate = bruteforce.findPrivate(serverPublic)
    print  "Brute force cracked the server's private key!"
    print "Server's private d equals " + str(serverPrivate)
    while RUNNING:
        message = s.recv(READ_SIZE)
        if message == "":
            break
        msg_list =[]
        for i in range(0, len(message), BLOCK_SIZE):
           msg_list.append(message[i: i + BLOCK_SIZE])
        decrypted_msg = ""
        for msg in msg_list:
           decrypted_msg += rsa.decrypt(int(msg), keys)
        if decrypted_msg == "message: quit\n\n":
            break  
        print remoteIP + ":" + remotePort + ": " + decrypted_msg
        if decrypted_msg.lower() == "quit":
            RUNNING = False
        

def main():
   keys = rsa.initializeKeys()
   public = keys[0]
   private = keys[1]
   myconnect(HOST, PORT)
   sendThread = Thread(target=send, args=(s, public))
   recvThread = Thread(target=recv, args=(s, private))
   sendThread.start()
   recvThread.start()
   recvThread.join()
   sendThread.join()
   s.close()
   sys.exit()
  

    
if __name__ == "__main__":
    main()
