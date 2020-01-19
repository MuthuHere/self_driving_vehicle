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
    if 'W' in keys:
        output = w
    elif 'A' in keys:
        output = a
    elif 'S' in keys:
        output = s
    elif 'D' in keys:
        output = d
    elif 'W' in keys and 'A' in keys:
        output = wa
    elif 'W' in keys and 'D' in keys:
        output = wd
    elif 'S' in keys and 'A' in keys:
        output = sa
    elif 'S' in keys and 'D' in keys:
        output = sd
    else:
        output = nk
    return output

file_name = 'training_data.npy'

#checking if there is already existing training data
if os.path.isfile(file_name):
    np_load_old = np.load
    # modify the default parameters of np.load
    np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
    # call load_data with allow_pickle implicitly set to true
    training_data = list(np.load(file_name))
    # restore np.load for future normal usage
    np.load = np_load_old
else:
    training_data = []

def main():
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    ##last_time = time.time()
    while True:
        if not paused:
            screen = grab_screen(region=(0,40,800,640))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            cv2.resize(screen, (80,60))
            keys = keycheck()
            output = outputkeys(keys)
            training_data.append([screen,output])

            if len(training_data)%100 == 0:
                print(len(training_data))
                np.save(file_name,training_data)

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

main()
