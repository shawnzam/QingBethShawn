"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamecheck
   Qing Xie"""

import socket
import SocketServer
import threading
import Queue

QUEUE = Queue()
#PUT HOST & PORT HERE
#What protocol are we using? 


def process_queue(client_socket, message):
    """Decodes the message in the queue"""
    #TODO: Fill in this function

class QueueThread(threading.Thread):
    """Decodes and processes client messages."""
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """Get each message off the queue and process it."""
        while True:
            process_queue(*QUEUE.get())
            QUEUE.task_done()

def ConnectionHandler(threading.Thread):
    """Handles each client's message by adding it to the queue"""
     def __init__(self, client_socket):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sock = client_socket

    def run(self):
        """Adds the client's message to the queue"""
        #TODO: Fill this in

def main():
    """Start the server and spawn threads to handle each request"""            
    # Set up the listening socket
    #http://docs.python.org/library/socketserver.html use as sample TCP
    
    HOST = 'localhost'
    PORT = 8282 #random port number, can change this
    listen_socket = SocketServer.TCPServer((HOST, PORT), ConnectionHandler)
    #listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #listen_socket.bind((HOST, PORT))
    #listen_socket.listen(1)
    

    # Start the thread to process the queue
    QueueThread().start()
    
    # Accept connections
   try:
      listen_socket.server_forever()
   except KeyboardInterrupt:
      pass
   finally:
      listen_socket.close()
    
   """ try:
        while True: 
            client, address = listen_socket.accept()
            #Spawn a thread as each client connects
            client_connection = ConnectionHandler(client)    
            client_connection.start()
    except KeyboardInterrupt:
        pass
    finally:
        listen_socket.close()"""
    
    
if __name__ == "__main__":
    main()
