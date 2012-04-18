"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""


import socket
from threading import Thread
import rsa

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
    s.connect((host, port))
    
def send (s, public_keys):
    global RUNNING
    send_key = str(public_keys[0]) + "," + str(public_keys[1])
    totalsent = 0
    while (totalsent < len(send_key)):
        sent = s.send(send_key[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
    
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
            
def recv(s, private_keys):
    global RUNNING
    print private_keys
    temp_public_key = ""
    temp_public_key += s.recv(READ_SIZE)
    k1 = temp_public_key.split(",")
    print k1
    global PUBLIC
    PUBLIC.append(int(k1[0]))
    PUBLIC.append(int(k1[1]))
    
    while RUNNING:
        message = s.recv(READ_SIZE)
        msg_list =[]
        for i in range(0, len(message), BLOCK_SIZE):
           msg_list.append(message[i: i + BLOCK_SIZE])
        print msg_list
        decrypted_msg = ""
        for msg in msg_list:
           decrypted_msg += rsa.decrypt(int(msg), private_keys)
        print decrypted_msg
        if decrypted_msg.lower() == "quit":
            RUNNING = False
        

def main():
    #s.connect((HOST, PORT))
    keys = rsa.initializeKeys()
    private = keys[1]  #I am going to use this to decrypt
    public = keys[0]  #send this to the client
    print "PUBLIC: "
    print public
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

