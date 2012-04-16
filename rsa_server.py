"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamecheck
   Qing Xie"""

import socket
import threading
import Queue
from rsa import all

QUEUE = Queue()
<<<<<<< HEAD
READ_SIZE = 1024
PORT = 8888
HOST = 'localhost'
BLOCK_SIZE = 10


class ConnectionHandler(threading.Thread):
=======


def process_queue(client_socket, message):
    """Decodes the message in the queue"""
    #TODO: Fill in this function

class QueueThread(threading.Thread):
    """Decodes and processes client messages."""
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

    def run(self):
        """Get each message off the queue and process it."""
        while True:
            process_queue(*QUEUE.get())
            QUEUE.task_done()

def ConnectionHandler(threading.Thread):
>>>>>>> 77d3f82cf142eeacfbf405e07dc01218e5c672f1
    """Handles each client's message by adding it to the queue"""
    def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sock = client_socket

    def run(self):
        """Reads in the client's message, decodes & sends back"""
        while True:
            #Read in message key
            msg_key = ""
            while("\n\n" not in msg_key):
                msg_key += self.sock.recv(READ_SIZE)
            #Read in the message
            msg = ""
            while("\n\n" not in msg_key):
                msg += self.sock.recv(READ_SIZE)
            msg_array = msg.split(" ")
            msg_list = map(''.join, zip(*[iter(msg_array)]*BLOCK_SIZE)) 
            for char in msg_list:
                decrypted_msg += decrypt(int(char), msg_key)
        print "Decrypted message: " + decrypted_msg 
                    
        
def main():
    """Start the server and spawn threads to handle each request"""            
    # Set up the listening socket
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
<<<<<<< HEAD
=======

    # Start the thread to process the queue
    QueueThread().start()
>>>>>>> 77d3f82cf142eeacfbf405e07dc01218e5c672f1
    
    # Accept connections
    try:
        while True: 
            client, address = listen_socket.accept()
            #Spawn a thread as each client connects
            conn = ConnectionHandler(client)    
            conn.start()
    except KeyboardInterrupt:
        pass
    finally:
        listen_socket.close()
    
    
if __name__ == "__main__":
    main()
