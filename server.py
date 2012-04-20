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
import socket
from threading import Thread
import rsa
import bruteforce

PUBLIC = []  #This is the client's public
READ_SIZE = 1024
BLOCK_SIZE = 10
HOST ="localhost"
PORT = 8888
RUNNING = True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#global socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



def myconnect(host, port):
    """Connection function.  Just connects to the specified host & port"""
    conn.connect((host, port))
    
def send (conn, public_keys):
    """Called by the send thread. This function sends its own public key to the client. It then enters a loop to read from the keyboard and write to the socket.
    It encrypts the message using the client's public key."""
    global RUNNING
    send_key = str(public_keys[0]) + "," + str(public_keys[1])
    totalsent = 0
    while (totalsent < len(send_key)):
        sent = conn.send(send_key[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent

    print "Public key sent"
    time.sleep(.1)#sleep used to clean up printing errors due to thread order.
    print "Enter a message: "
    while RUNNING:
        message = raw_input("")
        if message.lower() == "quit":
           RUNNING = False
           conn.close()
     
        totalsent = 0
        encryptedMessage = ''
        #Encrypt the message character by character
        for c in message:
            encryptedChunk = str(rsa.encrypt(c, PUBLIC))  
            neededZeros = BLOCK_SIZE - len(encryptedChunk)
            encryptedMessage += neededZeros * '0' + encryptedChunk
        try:
            #Try to send the message to the client
            while (totalsent < len(encryptedMessage)):
                sent = conn.send(encryptedMessage[totalsent:])
                if sent == 0:
                    raise socket.error
                totalsent = totalsent + sent
        except socket.error:
            print "Disconnecting... Goodbye."
            conn.close()

    conn.close()
            
def recv(conn, private_keys):
    """Called by the recv thread. This function receives the client's public key. It then enters a loop to read from the socket and write to the screen.
    It decrypts the message using its own public key."""
    global RUNNING
    global PUBLIC
    temp_public_key = ""
    temp_public_key += conn.recv(READ_SIZE)
    k1 = temp_public_key.split(",")

    PUBLIC.append(int(k1[0]))
    PUBLIC.append(int(k1[1]))
    print "Public key Received"
    time.sleep(.1)
    connDets = conn.getpeername()
    remoteIP = connDets[0]
    remotePort = str(connDets[1])
    print remoteIP + ":" + remotePort + " is connected"
    
    #Use brute force method to crack the client's private key
    clientPrivate = bruteforce.findPrivate(PUBLIC)
    print  "Brute force cracked the client's private key!"
    print "Client's private d equals " + str(clientPrivate)
    
    #While the client is connected, wait for messages
    while RUNNING:
        try:
            message = conn.recv(READ_SIZE)
        except socket.error:
            print "Disconnecting... Goodbye."
            conn.close()

        #Parse out the decoded message into preset block size 
        msg_list =[]
        for i in range(0, len(message), BLOCK_SIZE):
           msg_list.append(message[i: i + BLOCK_SIZE])
        decrypted_msg = ""

        #Decode the message.  Note that decrypt works in blocksize chunks
        for msg in msg_list:
           decrypted_msg += rsa.decrypt(int(msg), private_keys)
        print remoteIP + ":" + remotePort + ": " + decrypted_msg
        if decrypted_msg.lower() == "quit":
            print "Client exited. Type quit to close the server."
            RUNNING = False
            conn.close()
            
    #Close the socket if we managed to get out of while loop without closing        
    conn.close()
        

def main():
    keys = rsa.initializeKeys()
    private = keys[1]  #I am going to use this to decrypt
    public = keys[0]  #send this to the client
    print "Running the server..."
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
