'''

    RSA Key Generation program
    
    Key size is 1024-bits (default)
    The RabinMiller generates relatively very large prime numbers of order 2^keySize
    and the MathematicalCalculation checks for the GCD of keys.
    
'''

#import the necessary files
import random, GeneratePrime, MathematicalCalculation, sys, os

def main():
    print ("RSA Key Genarating...")
    key_file_name = input("Enter the starting name of the key file (Eg: key_file): ")
    makeKey(key_file_name, 1024)       #Key size is 1024-bits and name starts with key_file
    print ("Keyfile made...")

def generateKey(keySize):
    print ("Generating p...")
    p = GeneratePrime.generateLargePrime(keySize)         #Generate Very large prime numbers from Rabin Miller Algorithm
    print ("Generating q...")
    q = GeneratePrime.generateLargePrime(keySize)         #Generate very large prime numbers from Rabin Miller Algorithm

    n = p * q               #Calculate n
    fi = (p - 1) * (q - 1)  #Calculate fi(n)

    print ("Generating e that is co-prime with n and is less than fi(n)...")
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))        #Generate random range of numbers in range 2^(keysize-1) <= e <= 2^keysize
        if (MathematicalCalculation.gcd(e, fi) == 1):                                #if the gcd of the selected 'e' and fi returns true, break
            break

    print ("Generating d such that [(d * e) % fi = 1]...")
    d = MathematicalCalculation.findModInverse(e, fi)                    #calculate d using mod inverse formula

    publicKey = (n, e)
    privateKey = (n, d)

    print ("Public Key (n, e): ", publicKey)
    print ("Private Key (n, d): ", privateKey)

    return (publicKey, privateKey)

'''
    This function writes the key to a file.
    Public key to key_file_pubkey.txt
    Private key to key_file_privkey.txt
'''
def makeKey(name, keySize):
    try:
        #if the files already exist, generate error and exit
        if os.path.exists('%s_pubkey.txt'%(name)) or os.path.exists('%s_privkey.txt'%(name)):
            sys.exit("The file name already exist. Either rename the file or remove and re-run the program")
        publicKey, privateKey = generateKey(keySize)        #Generate key pairs
        print ("The public key is of length %s and a %s digit number."%(len(str(publicKey[0])), len(str(publicKey[1]))))
        print ("Writing it to public key file %s_pubkey.txt"%(name))

        #Write the public key to key_file_pubkey.txt
        try:
            with open ('%s_pubkey.txt'%(name), 'w') as data:
                data.write('%s, %s, %s'%(keySize, publicKey[0], publicKey[1]))
        except IOError as err:
            print ("File Error: " + str(err))
        
        print ("The private key is of length %s and a %s digit number."%(len(str(privateKey[0])), len(str(privateKey[1]))))
        print ("Writing it to private key file %s_privkey.txt"%(name))

        #Write the private key to key_file_privkey.txt
        try:
            with open ('%s_privkey.txt'%(name), 'w') as data:
                data.write('%s, %s, %s'%(keySize, privateKey[0], privateKey[1]))
        except IOError as er:
            print ("File Error: " + str(er))

    except Exception as e:
        print ("Error: " + str(e))

if __name__ == '__main__':
    main()
