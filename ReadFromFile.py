'''
    This file only contains a single function who's only purpose in life is to
    read the key files.
'''
import sys, pickle

def ReadFromFile(keyFile):
    try:
        with open (keyFile, 'rb') as data:
            content = pickle.load(data)
    except pickle.PickleError as pk:
        print ("File Error: " + str(pk))
        sys.exit()

    keySize, n, hashVal = content.split(',')

    return (int(keySize), int(n), int(hashVal))
