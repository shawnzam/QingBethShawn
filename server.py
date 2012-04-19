"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""

import socket
from threading import Thread
import rsa
import bruteforce

##Your Public keys are (43,10721).
##Your private keys are (3907,10721)
PUBLIC = []  #This is the client's public
READ_SIZE = 1024
BLOCK_SIZE = 10
HOST ="localhost"
PORT = 8888
RUNNING = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def myconnect(host, port):
    """The server's connection"""
    s.connect((host, port))
    
def send (s, public_keys):
    """Reads in a message from the server keyboard & sends to client"""
    global RUNNING

    #Send the server's public key to the client, so he can encrypt messages to server
    send_key = str(public_keys[0]) + "," + str(public_keys[1])
    totalsent = 0
    while (totalsent < len(send_key)):
        sent = s.send(send_key[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent

    #While the server & client are connected, accept messages from keyboard & send
    while RUNNING:
        message = raw_input("")
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
                sent = s.send(encryptedMessage[totalsent:])
                if sent == 0:
                    raise socket.error
                totalsent = totalsent + sent
        except socket.error:
            print "Disconnecting... Goodbye."
            s.close()

    s.close()
            
def recv(s, private_keys):
    """Thread that receives and prints all of the messages from the client."""
    global RUNNING
    global PUBLIC
    #Get the client's public key from the server & parse into global PUBLIC
    temp_public_key = ""
    temp_public_key += s.recv(READ_SIZE)
    client_public = temp_public_key.split(",")
    PUBLIC.append(int(client_public[0]))
    PUBLIC.append(int(client_public[1]))

    #Use brute force method to crack the client's private key
    clientPrivate = bruteforce.findPrivate(PUBLIC)
    print  "Brute force cracked the client's private key!"
    print "Client's private d equals " + str(clientPrivate)

    #While the client is connected, wait for messages
    while RUNNING:
        try:
            message = s.recv(READ_SIZE)
        except socket.error:
            print "Disconnecting... Goodbye."
            s.close()

        #Parse out the decoded message into preset block size 
        msg_list =[]
        for i in range(0, len(message), BLOCK_SIZE):
           msg_list.append(message[i: i + BLOCK_SIZE])
        decrypted_msg = ""

        #Decode the message.  Note that decrypt works in blocksize chunks
        for msg in msg_list:
           decrypted_msg += rsa.decrypt(int(msg), private_keys)
        print decrypted_msg
        if decrypted_msg.lower() == "quit":
            print "Client exited. Type quit to close the server."
            RUNNING = False
            s.close()
            
    #Close the socket if we managed to get out of while loop without closing        
    s.close()
        

def main():
    #s.connect((HOST, PORT))
    print "Running the server..."
    keys = rsa.initializeKeys()
    private = keys[1]  #I am going to use this to decrypt
    public = keys[0]  #Will send this to the client
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

