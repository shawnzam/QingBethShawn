"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""


import socket
import threading
import rsa

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def myconnect(host, port):
    s.connect((host, port))
    
def send(message, keys):
    totalsent = 0
    formattedMessage = "message: " + message + "\n\n"
    encryptedMessage = ''
    for c in formattedMessage:
            encryptedMessage += str(rsa.encrypt(c, keys[0])) + "," 
    while (totalsent < len(encryptedMessage)):
        sent = s.send(encryptedMessage[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
        print encryptedMessage
        return encryptedMessage

def main():
   keys = rsa.initializeKeys()
   myconnect("", 8888)
   msg = send("foobar", keys)
   decode = ''
   msgList = msg.split(",")
   del msgList[-1]     
   for c in msgList:
        decode += rsa.decrypt(int(c), keys[1])
   print decode       

if __name__ == "__main__":
    main()

