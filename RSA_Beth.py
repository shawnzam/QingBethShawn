# Elizabeth Cooper
#RSA_Beth.py

import random
import math
import RSAKey32 as RSAKey
import CRT


def euclid(a,b):
    #finds GCF
    while b > 0:
        (a,b) = (b, a % b) 
    return a
    #return RSAKey.euclid(a,b)

def coprime(L):
    F = [0]   
    #runs through all of the numbers in the list & stores their factors
    for i in range(0, len(L)):
        j = 2
        while(j <= (L[i])):
            if(L[i] % j == 0):
                F.append(j)
            j+=1      
    #checks to see if any of the factors are the same & returns False if they are & True if not
    F.sort()
    numSame = 0
    for i in range(0,(len(F)-1)):
        if(F[i] == F[i+1]):       
            numSame += 1
    if(numSame > 0):
        return False
    else:
        return True
    #return CRT.coprime(L)
    #return RSAKey.coprime(L)

def extendedEuclid(a,b):
    #call Euclid to get x = GCF
    gcf = euclid(a, b)
    y = 0; y1 = 1
    z = 1; z1 = 0
    #using the iterative method, computing y & z (note y1 & z1 are the i-1 case).  
    while b > 0:
        q = a // b              #q = quotient of a & b (cutting off decimal)
        (a,b) = (b, a % b)      #assigning b to a and b to a mod b
        (y, y1) = (y1 - q*y, y)         #assigning y to the last y - quotient*y. Once we do that, last y becomes y.
        (z, z1) = (z1 - q*z, z)         #assigning z to the last z- quotient*z.  Once we do that, last z becomes z.
    
    return (gcf, y1, z1)
    #return RSAKey.extendedEuclid(a,b)

def modInv(a,m):
    #call extendedEuclid to get GCF, y & z
    eEuclid = extendedEuclid(a, m)
    gcf = eEuclid[0]; y = eEuclid[1]; z = eEuclid[2]
    if gcf == 1:
        return y%m
    else:
        return 0
    #return RSAKey.modInv(a,m)

def crt(L):
    #break n's into a new list and check if they are coprime (n)
    #break out a's into new list (a)
    n = list(); a = list()
    for i in range(0, len(L)):
        n.append(L[i][1])
        a.append(L[i][0])
    if coprime(n)== False:
        print("The n's are not coprime! \n")
        return -1
    #finding M0, M1...Mi.  Assign each of the new values to M
    N = 1; M = list()
    for i in range(0, len(L)):
        N = N * n[i]
    for i in range(0, len(L)):
        M.append(N/n[i])
    #getting Y0,...Yi
    Y = list(); Y2 = list()
    for i in range(0, len(L)):
        Y.append(extendedEuclid(n[i],M[i]))
        Y2.append(Y[i][2])    
    #putting it all together to format x = a0M0Y0 + a1M1Y1 +...aiMiYi
    x = 0
    for i in range(0, len(L)):
        x = x + a[i] * M[i] * Y2[i]
    #simplifying x
    x = x % N
    return x
#   return RSAKey.crt(L)  

# start of second project *****************************

def extractTwos(m):
    #m is a positive integer. A tuple (s,d) of integers is returned
    #where m = (2^s)d and d is odd.
    if m < 0:
        m = abs(m)
    s = 0
    while m % 2 == 0:
        m = m / 2
        s += 1
    d = m
    
    return (s, d)
    #return RSAKey.extractTwos(m)   

def int2baseTwo(x):
    #returns a list of base 2 in REVERSE order
    baseTwoList = list()
    while x > 0:
        if x % 2 != 0:
            baseTwoList.append(1)
            x = x - 1
            x = x / 2
        else:
            baseTwoList.append(0)
            x = x / 2
            
    return baseTwoList
    #return RSAKey.int2baseTwo(x)   

def modExp(a,d,n):
    #returns a^d mod n. 
    dBaseTwo = int2baseTwo(d)
    aList = list()
    final = 1

    if len(dBaseTwo) == 1:
        aList.append(a)
    else:   
        #find all the modded exponents of a
        for i in range(0, len(dBaseTwo)-1):
            if i == 0:
                aList.append(a)
            newA = (a**2) % n
            a = newA
            aList.append(a)

    #check to see which powers to include. note lists are moving in reverse order from binary notation
    for i in range(0, len(dBaseTwo)):
        if dBaseTwo[i] == 1:
            final *= aList[i]
            final = final % n

    return final    
    #return RSAKey.modExp(a,d,n)    


def millerRabin(n, k):
    #returns true if probably prime & false if composite
    breakMarker = True
    count = 0
    if n == 2 or n ==3:
        return True
    if n % 2 == 0:
        return False
    m = n - 1
    s, d = extractTwos(m)
    random.seed()
 
    for i in range(0, k):
        breakMarker = True
        a = random.randint(2,n-2)
        x = modExp(a, d, n)  
        if x == 1 or x == n - 1:
            continue 
        else:
            #second for loop
            for r in range(1, s):
                if breakMarker == True:
                    x = modExp(x, 2, n)
                    if x == 1:
                        return False
                    elif x == n - 1:
                        breakMarker = False
                        break
            if breakMarker == True:
                return False
    return True
    #return RSAKey.millerRabin(n,k)


def primeSieve(k):
    #returns a list of k+1 elements. 1 indicates prime & 0 composite
    primeSieveList = list()    
    for i in range(0, k + 1):
        compositeCount = 0
        if i <= 1:
            primeSieveList.append(-1)
        elif i == 2:
            primeSieveList.append(1)
        else:
            for j in range(2, math.ceil(math.sqrt(i))+1):
                if i % j == 0:
                    #if we find a number that is divisible by j we increment counter
                    compositeCount += 1
            if compositeCount == 0:
                #if we find no factors, then append 1, otherwise append 0
                primeSieveList.append(1)
            else:
                primeSieveList.append(0)

    return primeSieveList        
    #return RSAKey.primeSieve(k)    
        
def findAPrime(a,b,k):
    #finds a prime number between a & b (or larger) and returns that number
    random.seed()
    n = random.randint(a, b)
    tries = 0
    
    while tries < (10 * math.log(n) +3):
        if millerRabin(n, k) == True:
            return n
        else:
            n += 1
            tries += 1
        
    failed = "We have failed to find a prime."
    return failed 
    #return RSAKey.findAPrime(a,b,k)
            
def newKey(a,b,k):
    #generates an RSA encryption/decryption key set
    #returns a tuple of (modulus, encryption exponent, private decryption exponent)
    p = findAPrime(a, b, k)
    q = findAPrime(a, b, k)
    while p == q:
        p = findAPrime(a, b, k)
        q = findAPrime(a, b, k)
        
    n = p * q   #modulus
    
    #finding e between 1 and (p-1)(q-1) & coprime to (p-1)(q-1)
    n1 = (p - 1) * (q - 1)
    e = findAPrime(1, n1, k)   #encryption exponent
    while euclid(e, n1) != 1:
        e = findAPrime(1, n1, k)

    #to find decryption exponent d*e = 1 mod n1
    d = modInv(e, n1)  #decryption exponent
    return (n, e, d)
    #return RSAKey.newKey(a,b,k)

def string2numList(strn):
    #converts a string (ascii char) to a list of numbers
    numList = list()
    for i in range(0, len(strn)):
        numList.append(ord(strn[i]))

    return numList
    #return RSAKey.string2numList(strn)    

def numList2string(L):
    #converts a list of numbers to a string
    string = ''
    for i in range(0, len(L)):
        string += chr(L[i])

    return string    
    #return RSAKey.numList2string(L)   

def numList2blocks(L,n):
    #converts a list, L of integers to blocks of size, n using base 256
    j = 0
    c = 1
    blockList = list()
    length = len(L)
    dividesEvenly = length % n
    random.seed()
    
    #check length of L & calc blocks if we can divide evenly into blocks.
    if dividesEvenly == 0:
        while length > 1:
            i = n
            e = n - 1
            blocks = 0
            while i > 0 :
                blocks += L[j] * 256**(e)
                j += 1
                i -= 1
                e -= 1
            blockList.append(blocks)
            length = length - n
            
    #if we can't divide into blocks, add random numbers to list to convert to blocks
    if dividesEvenly != 0:
        #find how many elements we need to add
        if n > length:
            difference = n - length
        nMultiple = n
        while nMultiple < length:
            c += 1
            nMultiple = n*c
        difference = nMultiple - length

        #append random numbers to the list to make it even
        for i in range(0, difference):
            L.append(random.randint(0, 127))
        j = 0
        length = len(L)
        #convert to blocks
        while length > 1:
            i = n
            e = n -1 
            blocks = 0
            while i > 0 :
                blocks += L[j] * 256**(e)
                j += 1
                i -= 1
                e -= 1
            blockList.append(blocks)
            length = length - n
    return blockList
    #return RSAKey.numList2blocks(L,n)

def blocks2numList(blocks,n):
    #converts blocks into integers (n in a list).  reverses numList2Blocks.
    length = len(blocks)
    exponent = n - 1
    numList = list()
    for i in range(0, length):
        while exponent >= 0:
            value = math.floor(blocks[i] / 256**exponent)
            blocks[i] = blocks[i] % 256**exponent
            numList.append(value)
            exponent -= 1
        exponent = n - 1
            
    return numList   
    #return RSAKey.blocks2numList(blocks,n)      

def encrypt(message, modN, e, blockSize):
    #encrypts a message
    numList = string2numList(message)
    blocks = numList2blocks(numList,blockSize)
    encryptedMessage = list()
       
    #c = m^e mod n
    for i in range(0, len(blocks)):
        encryptedMessage.append(modExp(blocks[i], e, modN))
    return encryptedMessage
    #return RSAKey.encrypt(message,modN,e,blockSize)

def decrypt(secret, modN, d, blockSize):
    #decrypts a messages
    m = list()

    #m = c^d mod n
    for i in range(0, len(secret)):
        decoded = modExp(secret[i], d, modN)
        m.append(decoded)
        
    numList = blocks2numList(m, blockSize)
    string = numList2string(numList)

    return string
    #return RSAKey.decrypt(secret, modN, d, blockSize)
        
