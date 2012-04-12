"""Chat server - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""


import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def myconnect(host, port):
    s.connect((host, port))
    
def send(message):
    totalsent = 0
    formattedMessage = "message: " + message + "\n\n"    
    while (totalsent < len(formattedMessage)):
        sent = s.send(formattedMessage[totalsent:])
        if sent == 0:
            raise RuntimeError("connection broken")
        totalsent = totalsent + sent
        print message


def main():
   myconnect("", 8888)
   send("foobar")

if __name__ == "__main__":
    main()
