import cv2
import numpy as np
import os
from readkeys import keycheck
import time

start = 1
file_name = 'training_data_{}.npy'.format(start)
np_load_old = np.load
# modify the default parameters of np.load
np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
paused = False

while os.path.isfile(file_name):
    training_data = np.load(file_name)
    for data in training_data:
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
        if not paused:
            img = data[0]
            key = data[1]
            ##img = cv2.resize(img, (800,600), interpolation = cv2.INTER_CUBIC)
            cv2.imshow('data', img)
            print(key)
            print(start)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    if not paused:
        start += 1
        file_name = 'training_data_{}.npy'.format(start)
# restore np.load for future normal usage
np.load = np_load_old
