"""Chat server - RSA Assignment.

   Beth Cooper

   Shawn Zamecheck

   Qing Xie"""



import socket

import threading

import Queue

import rsa  #Shawn's version

#from RSA_Beth import *



##Your Public keys are (43,10721).
##Your private keys are (3907,10721)
PUBLIC = [43, 10721]
PRIVATE = [3907,10721]
READ_SIZE = 1024
HOST = "localhost"
PORT = 8888
BLOCK_SIZE = 10





class ConnectionHandler(threading.Thread):

    """Handles each client's message by adding it to the queue"""

    def __init__(self, client_socket):

        threading.Thread.__init__(self)

        self.daemon = True

        self.sock = client_socket



    def run(self):

        """Reads in the client's message, decodes & sends back"""

        message = self.sock.recv(READ_SIZE)

        print "Encrypted Message: " + message

        #message = str(message)

        msg_list =[]

        for i in range(0, len(message), BLOCK_SIZE):

            msg_list.append(message[i: i + BLOCK_SIZE])

        print msg_list

        decrypted_msg = ""

        for msg in msg_list:

            decrypted_msg += rsa.decrypt(int(msg), PRIVATE[0], PRIVATE[1])
        print decrypted_msg


        #n = send("gotcha", PUBLIC, self.sock)
        self.sock.close()

                    

        

def send(message, keys, socket):
    totalsent = 0
    formattedMessage = "message: " + message + "\n\n"
    encryptedMessage = ''
    for c in formattedMessage:
        encryptedChunk = str(rsa.encrypt(c, PUBLIC))  
    	neededZeros = BLOCK_SIZE - len(encryptedChunk)
    	encryptedMessage += neededZeros * '0' + encryptedChunk
    while (totalsent < len(encryptedMessage)):
        sent = socket.send(encryptedMessage[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
        return encryptedMessage


def main():

    """Start the server and spawn threads to handle each request"""            

    # Set up the listening socket

    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listen_socket.bind((HOST, PORT))

    listen_socket.listen(1)

    

    # Accept connections

    try:

        while True: 

            client, address = listen_socket.accept()

            #Spawn a thread as each client connects

            conn = ConnectionHandler(client)

            print "Client Connected"

            conn.start()

    except KeyboardInterrupt:

        pass

    finally:

        listen_socket.close()

    

    

if __name__ == "__main__":

    main()

