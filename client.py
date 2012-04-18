"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""


import socket
from threading import Thread
import rsa
import sys

##Your Public keys are (43,10721).
##Your private keys are (3907,10721)
##PUBLIC = [43, 10721]
##PRIVATE = [3907,10721]
##SERVERPUBLIC = [49, 6437]
READ_SIZE = 1024
BLOCK_SIZE = 10
HOST ="localhost"
PORT = 8888
serverPublic = [0 for x in range(2)]
RUNNING = True

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def myconnect(host, port):
    s.connect((host, port))
    
def send (s, keys):
    global RUNNING
    mykeys = str(keys[0]) + "," + str(keys[1])
    print mykeys
    totalsent = 0
    while (totalsent < len(mykeys)):
        sent = s.send(mykeys[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
        
    while RUNNING:
        message = raw_input("")
        totalsent = 0
        #formattedMessage = "message: " + message + "\n\n"
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

def recv(s, keys):
    global serverPublic
    global RUNNING
    temp = s.recv(READ_SIZE)
    print temp
    tempPublic = temp.split(',')
    serverPublic[0] = int(tempPublic[0])
    serverPublic[1] = int(tempPublic[1])
    
    while RUNNING:
        message = s.recv(READ_SIZE)
        if message == "":
            break
        #print "Encrypted Message: " + message
        msg_list =[]
        for i in range(0, len(message), BLOCK_SIZE):
           msg_list.append(message[i: i + BLOCK_SIZE])
        #print msg_list
        decrypted_msg = ""
        for msg in msg_list:
           decrypted_msg += rsa.decrypt(int(msg), keys)
        if decrypted_msg == "message: quit\n\n":
            break  
        print decrypted_msg
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

