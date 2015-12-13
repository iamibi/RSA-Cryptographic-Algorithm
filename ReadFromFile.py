'''
    This file only contains a single function who's only purpose in life is to
    read the key files.
'''
import sys

def ReadFromFile(keyFile):
    try:
        with open (keyFile, 'r') as data:
            content = data.read()
    except IOError as err:
        print ("File Error: " + str(err))
        sys.exit()

    keyType, keySize, n, hashVal = content.split(',')

    return (int(keySize), int(n), int(hashVal))
