import win32api
import time

keylist = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'APS$/\\":
    keylist.append(char)

def keycheck():
    keys = []
    for key in keylist:
        if win32api.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys
