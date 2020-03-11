import numpy as np
from capture import grab_screen
import cv2
import time
from directinput import PressKey,ReleaseKey, W, A, S, D
from readkeys import keycheck
from statistics import mode,mean
import tensorflow as tf
from tensorflow.keras.models import load_model

tf.compat.v1.keras.backend.clear_session()
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
config.log_device_placement = True
sess = tf.compat.v1.Session(config=config)
tf.compat.v1.keras.backend.set_session(sess)

GAME_WIDTH = 1920
GAME_HEIGHT = 1080
WIDTH = 480
HEIGHT = 270

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

def straight():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)
    ReleaseKey(S)

def left():
    ReleaseKey(W)
    ReleaseKey(S)
    ReleaseKey(D)
    PressKey(A)
    #ReleaseKey(S)

def right():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    PressKey(D)
    
def brake():
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    PressKey(S)

def forward_left():
    ReleaseKey(D)
    ReleaseKey(S)
    PressKey(W)
    PressKey(A)
    
    
def forward_right():
    ReleaseKey(A)
    ReleaseKey(S)
    PressKey(W)
    PressKey(D)
    
def reverse_left():
    ReleaseKey(W)
    ReleaseKey(D)
    PressKey(S)
    PressKey(A)
    
def reverse_right():
    ReleaseKey(W)
    ReleaseKey(A)
    PressKey(S)
    PressKey(D)

def no_keys():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(S)
    ReleaseKey(D)
    

MODEL_NAME = 'model_gta_vgg16_v-1583788718.h5'
model = load_model(MODEL_NAME)

print('We have loaded a previous model!!!!')

def main():
    '''
    for i in list(range(7))[::-1]:
        print(i+1)
        time.sleep(1)
    '''

    paused = False
    mode_choice = 0

    while(True):
        
        if not paused:
            screen = grab_screen(region=(0,0,GAME_WIDTH,GAME_HEIGHT))
            screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
            screen = cv2.resize(screen, (WIDTH,HEIGHT))
            x_array = np.array(screen)
            x_array = x_array.reshape(-1,WIDTH,HEIGHT,3)
            #float_x_array = (tf.cast, tf.float32)
            x_array = x_array.astype('float32')
            prediction = model.predict(x_array)
            pred = np.argmax(prediction)
            #prediction = np.array(prediction) * np.array([0.1,0.5,0.5,0.5,1.8,1.8,0.5,0.5,0.1])

            mode_choice = np.argmax(prediction)
            print('Choice made: {}'.format(mode_choice))
            print('Prediction : {}'.format(pred))

            if mode_choice == 0:
                straight()
                choice_picked = 'straight'  
            elif mode_choice == 1:
                brake()
                choice_picked = 'reverse'  
            elif mode_choice == 2:
                left()
                choice_picked = 'left'
            elif mode_choice == 3:
                right()
                choice_picked = 'right'
            elif mode_choice == 4:
                forward_left()
                choice_picked = 'forward+left'
            elif mode_choice == 5:
                forward_right()
                choice_picked = 'forward+right'
            elif mode_choice == 6:
                reverse_left()
                choice_picked = 'reverse+left'
            elif mode_choice == 7:
                reverse_right()
                choice_picked = 'reverse+right'
            elif mode_choice == 8:
                no_keys()
                choice_picked = 'nokeys'
    
        keys = keycheck()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(A)
                ReleaseKey(W)
                ReleaseKey(D)
                ReleaseKey(S)
                time.sleep(1)

main()       