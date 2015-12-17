'''
    This file contains the decryption part of message
'''

#import the necessary files
import sys, pickle, ReadFromFile

DEFAULT = 128               #default block size
BYTE_SIZE = 256             #One byte contains 256 values according to ASCII

'''
    This method converts the blocks integers to their respective character
'''
def GetTextFromBlocks(decryptedBlocks, messageLen, blockSize = DEFAULT):
    message = []
    
    for blockInt in decryptedBlocks:
        blockMessage = []
        
        #Start the loop from end of the current block as ASCII numbers
        #are extracted from backwards from blockInt
        for i in range(blockSize - 1, -1, -1):
            
            #have we completed the message yet ?
            if (len(message) + i < messageLen):
                asciiVal = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiVal))           #Set the blockMessage list to insert the character always at starting

        message.extend(blockMessage)                            #append the message list

    #join() only works with strings
    return ''.join(message)

'''
    Use the formula m = c^d % n for decrypting the message
'''
def DecryptMessage(encryptedBlocks, messageLen, key, blockSize = DEFAULT):
    decryptedBlocks = []
    n, d = key

    #apply for every block
    for block in encryptedBlocks:
        decryptedBlocks.append(pow(block, d, n))

    return GetTextFromBlocks(decryptedBlocks, messageLen, blockSize)

'''
    Retrieve the key size, n, d from the key file
'''
def Decrypt(filename, keyFile):
    keySize, n, d = ReadFromFile.ReadFromFile(keyFile)

    #open the encrypted message file and read the data into the buffer
    try:
        with open(filename, 'rb') as data:
            content = pickle.load(data)
    except pickle.PickleError as pk:
        print ("File Error: " + str(pk))
        sys.exit()

    #split the data from content buffer
    messageLen, blockSize, encryptedMessage = content.split('_')
    messageLen = int(messageLen)        #convert from string to int
    blockSize = int(blockSize)          #convert from string to int

    if keySize < blockSize * 8:
        sys.exit("ERROR: Block Size is %s-bits and key size is %s-bts. The RSA-Cipher requires the block size to be equal to or less than the key size."%(blockSize * 8, keySize))

    encryptedBlocks = []
    
    #Extract the block from the encrypted message file
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    decryptedContent = DecryptMessage(encryptedBlocks, messageLen, (n, d), blockSize)

    #write the decrypted message to a file
    try:
        with open ('decrypted_file.pickle', 'wb') as data1:
            pickle.dump(decryptedContent, data1)
    except pickle.PickleError as pk1:
        print ("File Error: " + str(pk1))
    
    return decryptedContent
