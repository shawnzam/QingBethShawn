"""
Chat Server - RSA Assignment.
Beth Cooper
Shawn Zamechek
Qing Xie

Threaded Chat Server. There is a thread to read from the keyboard and
write to the socket and another thread to read from the socket and print to the screen.
The send thread sends the public key to the server while the recv thread receives the client's
public key and assigns the key to the global variable PUBLIC. 
"""

import socket, time
from threading import Thread
import rsa

PUBLIC = []  #This is the client's public
READ_SIZE = 1024
BLOCK_SIZE = 10
HOST ="localhost"
PORT = 8888
RUNNING = True



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#global socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


"""
I do not the like passing one param with a comma separator, Seems confusing so wrote my own version of connect 
"""
def myconnect(host, port):
    s.connect((host, port))
    
"""
Called by the send thread. This function sends its own public key to the client. It then enters a loop to read from the keyboard and write to the socket. It encrypts the message using the client's public key.
"""
def send (s, public_keys):
    global RUNNING
    send_key = str(public_keys[0]) + "," + str(public_keys[1])
    totalsent = 0
    while (totalsent < len(send_key)):
        sent = s.send(send_key[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
    print "Public key sent"
    time.sleep(.1)#sleep used to clean up printing errors due to thread order.
    print "Enter a message: "
    while RUNNING:
        message = raw_input("")
        totalsent = 0
        encryptedMessage = ''
        for c in message:
            encryptedChunk = str(rsa.encrypt(c, PUBLIC))  
            neededZeros = BLOCK_SIZE - len(encryptedChunk)
            encryptedMessage += neededZeros * '0' + encryptedChunk
        while (totalsent < len(encryptedMessage)):
            sent = s.send(encryptedMessage[totalsent:])
            if sent == 0:
                raise RuntimeError("connection broken")
            totalsent = totalsent + sent
            
"""
Called by the recv thread. This function receives the client's public key. It then enters a loop to read from the socket and write to the screen. It decrypts the message using its own public key.
"""
def recv(s, private_keys):
    global RUNNING
    #print private_keys
    temp_public_key = ""
    temp_public_key += s.recv(READ_SIZE)
    k1 = temp_public_key.split(",")
    #print k1
    global PUBLIC
    PUBLIC.append(int(k1[0]))
    PUBLIC.append(int(k1[1]))
    print "Public key Received"
    time.sleep(.1)
    connDets = s.getpeername()
    remoteIP = connDets[0]
    remotePort = str(connDets[1])
    print remoteIP + ":" + remotePort + " is connected"
    while RUNNING:
        message = s.recv(READ_SIZE)
        msg_list =[]
        for i in range(0, len(message), BLOCK_SIZE):
           msg_list.append(message[i: i + BLOCK_SIZE])
        decrypted_msg = ""
        for msg in msg_list:
           decrypted_msg += rsa.decrypt(int(msg), private_keys)
        print remoteIP + ":" + remotePort + ": " + decrypted_msg
        if decrypted_msg.lower() == "quit":
            RUNNING = False
        

def main():
    keys = rsa.initializeKeys()
    private = keys[1]  #I am going to use this to decrypt
    public = keys[0]  #send this to the client
    s.bind((HOST, PORT))
    s.listen(1)
    conn, address = s.accept()
    sendThread = Thread(target=send, args=(conn, public))
    recvThread = Thread(target=recv, args=(conn, private))
    sendThread.start()
    recvThread.start()
    sendThread.join()
    recvThread.join()
   
  

    
if __name__ == "__main__":
    main()
