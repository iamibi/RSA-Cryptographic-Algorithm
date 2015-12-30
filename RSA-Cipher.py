'''
    This file contains the main program that is to be run after the key files
    have been generated.
'''

#import the necessary files
import sys, os, pickle, EncryptMessage, DecryptMessage

def main():
    print ("RSA ASYMMETRIC CRYPTOGRAPHIC ALGOROTHM")
    mode = input("Enter the mode (Encrypt or Decrypt): ")       #Choose between encrypt or decrypt
    filename = 'encrypted_file.pickle'                                 #encrypted message file name
    
    try:
        with open('key.pickle', 'rb') as keyCheck:
            KEY = pickle.load(keyCheck)
    except pickle.PickleError as pick:
        print ("Key File Error: " + str(pick))
        sys.exit()
    
    KEY = KEY.split(',')
    #if the user want to encrypt a message
    if mode[0] in 'E e'.split():
        dg = input("Do you want to digitally sign the message? [Yes/No]: ")
        if dg[0] in 'Y y'.split():
            key_file = KEY[1]
        elif dg[0] in 'N n'.split():
            key_file = KEY[0]
        else:
            sys.exit("Invalid entry...Exiting")
        if not (os.path.exists(key_file)):
            key_file = input("Enter the public key file name with extension: ")
            
            if not (os.path.exists(key_file)):
                sys.exit("The file %s doesn't exist. First run keyGenerate.py..."%(key_file))
        
        #Enter the message and write it to a file
        message = input("Enter the message that you want to encrypt: ")
        print ("Encrypting and writing to the file %s..."%(filename))
        encrypted_message = EncryptMessage.Encrypt(message, filename, key_file)
        print ("Encrypted message: %s"%(encrypted_message))
        
    #else if the user want to decrypt the message
    elif mode[0] in 'D d'.split():
        dg = input("Is your message digitally signed? [Yes/No]: ")
        if dg[0] in 'Y y'.split():
            flag_k = 1
        elif dg[0] in 'N n'.split():
            flag_k = 0
        else:
            sys.exit("Invalid Entry...Exiting")

        if flag_k == 1:
            key_file = KEY[0]
        elif flag_k == 0:
            key_file = KEY[1]
        print (key_file)
        if not (os.path.exists(filename)):
            sys.exit("The encrypted message file %s doesn't exist..."%(filename))

        if not (os.path.exists(key_file)):
            key_file = input("Enter the private key file name with extension: ")
            if not (os.path.exists(key_file)):
                sys.exit("The file %s doesn't exist. First run keyGenerate.py..."%(key_file))

        print ("Decrypting and Writing to the file decrypted_file.pickle")
        
        decrypted_message = DecryptMessage.Decrypt(filename, key_file)
        print ("Decrypted message: %s"%(decrypted_message))
    else:
        print ("Invalid Choice...Exiting")
        sys.exit()

if __name__ == '__main__':
    main()
