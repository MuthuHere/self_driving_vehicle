import numpy as np
import cv2
import time
import os
import pandas as pd
from tqdm import tqdm
from collections import deque
from new_model import inception_v3
from random import shuffle


FILE_I_END = 149
v = 1

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 30

MODEL_NAME = 'model_gta_v2-{}'.format(v)
PREV_MODEL = 'model_gta_v-{}'.format(v-1)

LOAD_MODEL = False

wl = 0
sl = 0
al = 0
dl = 0

wal = 0
wdl = 0
sal = 0
sdl = 0
nkl = 0

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

model = inception_v3(WIDTH, HEIGHT, 3, LR, output=9)

if LOAD_MODEL:
    model.load(PREV_MODEL)
    print('We have loaded a previous model!!!!')
    

# iterates through the training files


for e in range(EPOCHS):
    data_order = [i for i in range(1,FILE_I_END+1)]
    shuffle(data_order)
    for count,i in enumerate(data_order):
        try:
            file_name = 'training_data_{}.npy'.format(i)
            train_data = np.load(file_name, allow_pickle=True)
            shuffle(train_data)
            train_set = train_data[:-50]
            test_set = train_data[-50:]
            X = np.array([i[0] for i in train_set]).reshape(-1,WIDTH,HEIGHT,3)
            Y = [i[1] for i in train_set]

            test_x = np.array([i[0] for i in test_set]).reshape(-1,WIDTH,HEIGHT,3)
            test_y = [i[1] for i in test_set]

            model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),  snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)


            if count%10 == 0:
                print('SAVING MODEL!')
                model.save(MODEL_NAME)
                    
        except Exception as e:
            print(str(e))
            
    









#tensorboard --logdir=foo:C:/Users/H/Desktop/ai-gaming-phase7/log