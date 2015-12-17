'''
    This file contains all the necessary functions for encrypting the message
'''

#import the necessary files
import sys, pickle, ReadFromFile

DEFAULT = 128           #default block size
BYTE_SIZE = 256         #One byte has 256 different values according to ASCII

'''
    Convert the message in the block form
'''
def GetBlocksFromText(message, blockSize = DEFAULT):
    #encode the message from string to ascii bytes
    messageBytes = message.encode('ascii')
    
    blockInteger = []
    
    #do it block-by-block
    for start in range (0, len(messageBytes), blockSize):
        blockInt = 0
        
        #use the formula (current letter x 256^index of the letter)
        #to convert normal ascii number to a big value
        for i in range (start, min(start + blockSize, len(messageBytes))):
            blockInt = blockInt + messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInteger.append(blockInt)

    return blockInteger

'''
    Encrypt the message block using the formula c = (m ^ e) % n
'''
def EncryptMessage(message, key, blockSize = DEFAULT):
    encrBlock = []
    n, e = key

    for block in GetBlocksFromText(message, blockSize):
        encrBlock.append(pow(block, e, n))

    return encrBlock

'''
    Get the key file and check whether the block size is equal to or less than key size
'''
def Encrypt(message, filename, keyFile, blockSize = DEFAULT):
    #imported file
    keySize, n, e = ReadFromFile.ReadFromFile(keyFile)

    #check for block size
    if keySize < blockSize * 8:
        sys.exit("ERROR: Block size is %s-bits and key size is %s-bits. RSA cipher requires the block size to be equal to or less than the key size."%(blockSize * 8, keySize))
    
    #encrypted block
    encrypted_block = EncryptMessage(message, (n, e), blockSize)

    #convert the bytes form of message to string
    for i in range (len(encrypted_block)):
        encrypted_block[i] = str(encrypted_block[i])

    #if the message was greater than one block
    encrypted_content = ','.join(encrypted_block)
    encrypted_content = '%s_%s_%s'%(len(message), blockSize, encrypted_content)
    
    #write the encrypted message to a file
    try:
        with open(filename, 'wb') as encrpM:
            pickle.dump(encrypted_content, encrpM)
    except pickle.PickleError as pk:
        print ("File Error: " + str(pk))

    return encrypted_content
