import re, sys, fractions, random, math

#This is Beth! Testing updating file!
#This is Qing!let's try it again~
public = [0 for x in range(2)]
private = [0 for x in range(2)]
def isPrime(n):
    """Checks if a number is prime"""
    # see http://www.noulakaz.net/weblog/2007/03/18/a-regular-expression-to-check-for-prime-numbers/
    return re.match(r'^1?$|^(11+?)\1+$', '1' * n) == None

def getprimes(m, n):
    primes = [0 for x in range(2)]
    count = 0
    index = 0
    while (m != count):
 
        if (isPrime(index)):
            count = count + 1
        primes[0] = index
        index = index + 1
    count = 0
    index = 0
    while (n != count):
       
        if (isPrime(index)):
            count = count + 1
        primes[1] = index 
        index = index + 1
    return primes
    

def computekeys(primes):
     global public
     global private
     a = primes[0]
     b = primes[1] 
     c = a * b
     m = (a-1)*(b-1)
     e = coprime(m)
     d = modInverse(e, m)
     public = [e, c]
     private = [d, c]
            
    
def coprime(x):
    cp = random.randint(1, 100)
    while (fractions.gcd(cp, x) != 1):
        cp = random.randint(1, 100)
    return cp

def modInverse(a,m) :
  """Computes the modular multiplicative inverse of a modulo m,
     using brute force"""
  a %= m
  for x in range(1,m) :
    if a*x%m == 1 :
       return x
  return None

def encrypt(c, public):
    """Encrypts the message"""
    #global public
    #print "encrypting {0} with ({1},{2})".format(c,public[0],public[1])
    ansii = ord(c)
    #print ansii
    encrypt =(ansii**public[0])%public[1]
    return encrypt

def decrypt(ch, private):
    """Decrypts the message"""
    #global private
    d = private[0]  
    c = private[1]
    #print "decrypting {0} with ({1},{2})".format(ch,d,c)
    d = int(d)
    c = int(c)
    ch = int(ch)
    temp = (ch**d)%c
    return chr(temp)
        
def initializeKeys():
    """Initializes the public & private keys"""
    x = getprimes(random.randint(5, 100),(random.randint(5, 100)))
    computekeys(x)
    
    print "Your Public keys are ({0},{1}).\nYour private keys are ({2},{3}).".format(public[0],public[1],private[0], private[1])
    return [public, private]
    ##for c in msg:
      ##  temp = encrypt(c)
      ##  rmsg += decrypt(temp)
    ##print rmsg


