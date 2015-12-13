'''
    This file contains the main program that is to be run after the key files
    have been generated.
'''

#import the necessary files
import sys, os, EncryptMessage, DecryptMessage

flag = 0                                                        #set the flag for digital signature

def main():
    print ("RSA ASYMMETRIC CRYPTOGRAPHIC ALGOROTHM")
    mode = input("Enter the mode (Encrypt or Decrypt): ")       #Choose between encrypt or decrypt
    filename = 'encrypted_file.txt'                             #encrypted message file name
    key_file = ''
    
    #if the user want to encrypt a message
    if mode[0] in 'E e'.split():
        key_file = "key_file_pubkey.txt"
        if not (os.path.exists(key_file)):
            key_file = input("Enter the public key file name with extension: ")
            
            if not (os.path.exists(key_file)):
                sys.exit("The file %s doesn't exist. First run keyGenerate.py..."%(key_file))
                
            #check whether the user want to digitally sign the message
            CheckKeyFile('Encrypt', key_file, 'Kv', 'Private Key')
        
        #Enter the message and write it to a file
        message = input("Enter the message that you want to encrypt: ")
        print ("Encrypting and writing to the file %s..."%(filename))
        encrypted_message = EncryptMessage.Encrypt(message, filename, key_file)
        print ("Encrypted message: %s"%(encrypted_message))
        
    #else if the user want to decrypt the message
    elif mode[0] in 'D d'.split():
        key_file = "key_file_privkey.txt"
        if not (os.path.exists(filename)):
            sys.exit("The encrypted message file %s doesn't exist..."%(filename))

        if (not (os.path.exists(key_file)) or flag):
            key_file = input("Enter the private key file name with extension: ")
            if not (os.path.exists(key_file)):
                sys.exit("The file %s doesn't exist. First run keyGenerate.py..."%(key_file))
        
            #if the file was digitally signed
            CheckKeyFile('Decrypt', key_file, 'Kp', 'Public Key')

        print ("Decrypting and Writing to the file decrypted_file.txt")
        
        decrypted_message = DecryptMessage.Decrypt(filename, key_file)
        print ("Decrypted message: %s"%(decrypted_message))
    else:
        print ("Wrong Choice...Exiting")
        sys.exit()

def CheckKeyFile(mode, key_file, key, key_type):
    flag = 1
    try:
        with open (key_file, 'r') as fo:
            content = fo.read()
            if key in content:
                print ("Are you sure you want to %s the message using %s(Digital Signature) [Yes/No]: "%(mode, key_type), end = '')
                ch = input()
                if ch in "Yes yes y Y".split():
                    print ("Digital Signature.....[Selected]")
                elif ch in "No no n N".split():
                    sys.exit ("Re-run the program with correct file name")
                else:
                    sys.exit ("Invalid Choice...Exiting")
    except IOError as er:
        print ("File Error: " + str(er))
        sys.exit()

if __name__ == '__main__':
    main()
