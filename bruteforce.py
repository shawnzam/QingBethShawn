import math

def bruteForce(number):
    for i in range (2 ,(int)(math.sqrt(number))):
        if number%i == 0:
            return i

    return -1
        
    
    
