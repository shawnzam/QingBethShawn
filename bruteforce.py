"""Brute Force Solver - RSA Assignment.
   Beth Cooper
   Shawn Zamechek
   Qing Xie"""

import math
import rsa

PUBLIC_KEY = [79, 14921]
PRIVATE_KEY = [3679, 14921]
BLOCK_SIZE = 10
""" public = [e, c]
    private = [d, c]"""

def bruteForce(number):
    """Finds p by brute force"""
    for i in range (2 ,(int)(math.sqrt(number))):
        if number%i == 0:
            return i
    return -1

def findPrivate(public_key):
    """Finds the private key, d. Parameter is an array of [e, c]"""
    e = public_key[0]
    c = public_key[1]
    
    p = bruteForce(c)
    if p == -1:
        print "Unable to factor public key"
        raise ValueError #TODO - should this be value error
    q = c / p
    m = (p - 1) * (q -1)
    d = rsa.modInverse(e, m)

    return d

        
def main():
    """Main just used for testing"""
    global PUBLIC_KEY
    global BLOCK_SIZE
    
    public = [PUBLIC_KEY[0], PUBLIC_KEY[1]]
    e = PUBLIC_KEY[0]
    c = PUBLIC_KEY[1]s
    d = findPrivate(public)

    first_msg = "Hello world"
    encryptedMessage = ""
    decryptedMessage = ""
    
    for char in first_msg:
        block = str(rsa.encrypt(char, public))  
        neededZeros = BLOCK_SIZE - len(block)
        encryptedMessage += neededZeros * '0' + block
    print encryptedMessage

    msg_list =[]
    for i in range(0, len(encryptedMessage), BLOCK_SIZE):
       msg_list.append(encryptedMessage[i: i + BLOCK_SIZE])

    print "Message list"
    print msg_list
    for msg in msg_list:
        decryptedMessage += rsa.decrypt(int(msg), [d, c])
    print "Decrypted " + str(decryptedMessage)
    
    
    
if __name__ == "__main__":
    main()
    
