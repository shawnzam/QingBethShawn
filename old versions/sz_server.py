"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""


import socket
from threading import Thread
import rsa
import sys


Your Public keys are (49,6437).
Your private keys are (2929,6437).
PUBLIC = [49, 6437]
CLIENTPUBLIC = [43, 10721]
PRIVATE =[2929, 6437]
READ_SIZE = 1024
BLOCK_SIZE = 10
HOST ="localhost"
PORT = 8888


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def myconnect(host, port):
    s.connect((host, port))
    
def send (s, keys):
    while 1:
        message = raw_input("")
        if message == "quit":
            break
        totalsent = 0
        #formattedMessage = "message: " + message + "\n\n"
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
def recv(s, keys):
    while 1:
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
           decrypted_msg += rsa.decrypt(int(msg), PRIVATE[0], PRIVATE[1])
        if decrypted_msg == "message: quit\n\n":
            break   
        print decrypted_msg
        

def main():
   s.bind((HOST, PORT))
   s.listen(1)
   conn, address = s.accept()
   sendThread = Thread(target=send, args=(conn, PUBLIC))
   recvThread = Thread(target=recv, args=(conn, PUBLIC))
   recvThread.start() 
   sendThread.start()
   recvThread.join()
   sendThread.join()
   conn.close()
   sys.exit()
   
  

    
if __name__ == "__main__":
    main()

