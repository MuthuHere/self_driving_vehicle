import numpy as np
import cv2
import time
import pyautogui
from directinput import PressKey,ReleaseKey, W, A, S, D
from lanes import draw_lanes
from capture import grab_screen
from readkeys import keycheck
import os

w = [1,0,0,0,0,0,0,0,0]
a = [0,1,0,0,0,0,0,0,0]
s = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

def outputkeys(keys):
    #         w,a,s,d,wa,wd,sa,sd,nk
    output = [0,0,0,0,0,0,0,0,0]
    if 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    elif 'W' in keys:
        output = w
    elif 'A' in keys:
        output = a
    elif 'S' in keys:
        output = s
    elif 'D' in keys:
        output = d
    else:
        output = nk
    return output

#splitting into multiple files to handle the volume of data
start = 1
file_name = 'training_data_{}.npy'.format(start)

#checking if there is already existing training data
while True:
    if os.path.isfile(file_name):
        start += 1
        file_name = 'training_data_{}.npy'.format(start)
    else:
        print('Staring')
        break


def main(filename, startval):
    file_name = filename
    start = startval
    training_data = []

    #Countdown delay
    for i in list(range(7))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    ##last_time = time.time()
    while True:
        if not paused:
            screen = grab_screen(region=(0,0,1920,1080))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            screen = cv2.resize(screen, (80,60))
            keys = keycheck()
            output = outputkeys(keys)
            training_data.append([screen,output])

##            if len(training_data)%100 == 0:
##                print(len(training_data))

            if len(training_data) == 500:
                print(start)
                np.save(file_name, training_data)
                start += 1
                training_data = []
                file_name = 'training_data_{}.npy'.format(start)

        keys = keycheck()
        if 'T' in keys:
            if paused:
                paused = False
                print('Resume')
                time.sleep(1)
            else:
                paused = True
                print('Pause')
                time.sleep(1)
        ##print('Frame took {} seconds'.format(time.time()-last_time))
        ##last_time = time.time()

main(file_name, start)
