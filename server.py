"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""


import socket
from threading import Thread
import rsa

##Your Public keys are (43,10721).
##Your private keys are (3907,10721)
PUBLIC = [43, 10721]  #This is the client's public
PRIVATE = [257,6739]  #This is my private key
READ_SIZE = 1024
BLOCK_SIZE = 10
HOST ="localhost"
PORT = 8888


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


def myconnect(host, port):
    s.connect((host, port))
    
def send (s, public_keys, private_keys):
    print "public: " + str(public_keys[0])
    send_key = str(public_keys[0]) + "," + str(public_keys[1])
    while (totalsent < len(send_key)):
        sent = s.send(send_key[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
    
    while 1:
        message = raw_input("")
        totalsent = 0
        formattedMessage = "message: " + message + "\n\n"
        encryptedMessage = ''
        for c in formattedMessage:
            encryptedChunk = str(rsa.encrypt(c, PUBLIC))  
            neededZeros = BLOCK_SIZE - len(encryptedChunk)
            encryptedMessage += neededZeros * '0' + encryptedChunk
        while (totalsent < len(encryptedMessage)):
            sent = s.send(encryptedMessage[totalsent:])
            if sent == 0:
                raise RuntimeError("connection broken")
            totalsent = totalsent + sent
            
def recv(s, private_keys):
    print private_keys
    temp_public_key = ""
    temp_public_key += s.recv(READ_SIZE)
    k1 = temp_public_key.split(",")
    PUBLIC[0] = int(k1[0])
    PUBLIC[1] = int(k1[1])
    
    while 1:
        message = s.recv(READ_SIZE)
        print "Encrypted Message: " + message
        msg_list =[]
        for i in range(0, len(message), BLOCK_SIZE):
           msg_list.append(message[i: i + BLOCK_SIZE])
        print msg_list
        decrypted_msg = ""
        for msg in msg_list:
           decrypted_msg += rsa.decrypt(int(msg), private_keys)
        print decrypted_msg
        

def main():
    #s.connect((HOST, PORT))
    keys = rsa.initializeKeys()
    private = keys[1]  #I am going to use this to decrypt
    PRIVATE = keys[1]
    public = keys[0]  #send this to the client
    print "PUBLIC: "
    print public
    s.bind((HOST, PORT))
    s.listen(1)
    conn, address = s.accept()
    sendThread = Thread(target=send, args=(conn, public, private))
    recvThread = Thread(target=recv, args=(conn, private))
    sendThread.start()
    recvThread.start()
    sendThread.join()
    recvThread.join()
   
  

    
if __name__ == "__main__":
    main()

