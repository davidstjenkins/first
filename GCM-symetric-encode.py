#!/usr/bin/env python

import base64
from pickle import load, dump
from os import popen, path
from binascii import a2b_qp, a2b_hex, b2a_qp, b2a_hex, b2a_base64, a2b_base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# This is the starting point

def encrypt(key, iv, plaintext, associated_data):
    # Generate a random 96-bit IV.

    # Construct an AES-GCM Cipher object with the given key and a
    # randomly generated IV.
    encryptor = Cipher(
        algorithms.AES(a2b_hex(key)),
        modes.GCM(a2b_hex(iv)),
        backend=default_backend()
    ).encryptor()

    # associated_data will be authenticated but not encrypted,
    # it must also be passed in on decryption.
    encryptor.authenticate_additional_data(associated_data)

    # Encrypt the plaintext and get the associated ciphertext.
    # GCM does not require padding.
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return (ciphertext, encryptor.tag)

def decrypt(key, associated_data, iv, ciphertext, tag):
    # Construct a Cipher object, with the key, iv, and additionally the
    # GCM tag used for authenticating the message.
    decryptor = Cipher(
        algorithms.AES(a2b_hex(key)),
        modes.GCM(a2b_hex(iv), tag),
        backend=default_backend()
    ).decryptor()

    # We put associated_data back in or the tag will fail to verify
    # when we finalize the decryptor.
    decryptor.authenticate_additional_data(associated_data)

    # Decryption gets us the authenticated plaintext.
    # If the tag does not match an InvalidTag exception will be raised.
    return decryptor.update(ciphertext) + decryptor.finalize()

def new_key():
    k = popen('dd if=/dev/random bs=32 count=1 2>/dev/null | xxd -p -c32 | tr -d "\n"').read()
    return(k)

def iv_test(iv):
    iv = iv + '\n'
    if path.isfile('myivs.lst') == False:
        f = open('myivs.lst', 'w')
        f.write(iv)
        f.close()
        return(True)
    f = open('myivs.lst', 'r')
    #debug
    for i in f:
        print(i)
    if iv in f:
        return(False)
    else:
        L = []
        f = open('myivs.lst', 'r')
        for l in f:
            if 0 != len(l):
                L.append(l)
        f.close()
        L.append(iv)
        f = open('myivs.lst', 'w')
        for i in L:
            f.write(i)
        f.close()
        return(True)

def unique_iv():
    vector = popen('dd if=/dev/random bs=12 count=1 2>/dev/null | xxd -p -c32 | tr -d "\n"').read()

    if iv_test(vector):
        return(vector)
    else:
        unique_iv()

def key_management(key):
    key = key + '\n'
    if path.isfile('mykeys.lst') == False:
        f = open('mykeys.lst', 'w')
        f.write(key)
        f.close()
    else:
        L = []
        f = open('mykeys.lst', 'r')
        for l in f:
            if 0 != len(l):
                L.append(l)
        f.close()
        L.append(key)
        f = open('mykeys.lst', 'w')
        for i in L:
            f.write(i)
        f.close()
    f = open('mykeys.lst', 'r')
    for i in f:
        print(i)
    choice = input('Which key do you want: ')
    print(choice)
    return(choice)
   
def main():
    n_k = new_key()
    k = key_management(n_k)
    vector = unique_iv()

#    source = input("Enter the name of the file to be encrypted: ")
#    if path.isfile(source) != True:
#        print("No such file.")
#        exit(2)
    source = input("Enter the text to be encrypted: ")
    print("The filename for the encrypted text: %s" % vector)
    # Do I want to use the IV for the file name?
    target = vector + '.enc'
    tagget = vector + '.tag'
    line1 = source.rstrip('\n')
    line2 = a2b_qp(line1)
    ciphertext, tag = encrypt(
            k,
            vector,
            line2,
            b"authenticated but not encrypted payload"
        ) 
    dump(ciphertext, open(target, 'wb'))
    dump(tag, open(tagget, 'wb'))
    #print("Key = %s" % k)
    #print("Initializing vector = %s" % vector)
    #print("The encrypted text: %s" % ciphertext)
    
    hidden  = input("Enter the name of the file to be decrypted: ")
    if path.isfile(hidden) != True:
        print("No such file.")
        exit(2)
    hidtag  = input("Enter the name of the tag file of the encrypted file: ")
    if path.isfile(hidtag) != True:
        print("No such file.")
        exit(2)

    line1 = load(open(hidden, 'rb'))
    lin3 = load(open(hidtag, 'rb'))
    messageline = decrypt(
            k,
            b"authenticated but not encrypted payload",
            vector,
            line1,
            lin3
            )
    print("The original message: %s" % messageline)

if "__main__" == __name__:
    main()
