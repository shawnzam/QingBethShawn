"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""


import socket
import threading
import rsa


BLOCK_SIZE = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def myconnect(host, port):
    s.connect((host, port))
    
def send(message, keys):
    totalsent = 0
    formattedMessage = "message: " + message + "\n\n"
    encryptedMessage = ''
    for c in formattedMessage:
        encryptedChunk = str(rsa.encrypt(c, keys[0]))  
    	neededZeros = BLOCK_SIZE - len(encryptedChunk)
    	encryptedMessage += neededZeros * '0' + encryptedChunk
    while (totalsent < len(encryptedMessage)):
        sent = s.send(encryptedMessage[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
        return encryptedMessage

def main():
   keys = rsa.initializeKeys()
   myconnect("", 8888)
   msg = send("hello", keys)
   decode = ''
   msgList = map(''.join, zip(*[iter(msg)]*BLOCK_SIZE))   
   for c in msgList:
        decode += rsa.decrypt(int(c), keys[1])
   print decode       



if __name__ == "__main__":
    main()

