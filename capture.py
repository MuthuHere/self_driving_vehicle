import numpy as np
import cv2
from PIL import ImageGrab
import time

last_time = time.time()
while(True):
    printscreen_pil = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))## converting to np array here to prevent low fps caused by pil
##    printscreen_numpy = np.array(printscreen_pil.getdata(),dtype='uint8').reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))
    print('Loop took {} second'.format(time.time()-last_time))
    last_time = time.time()
    cv2.imshow('window',cv2.cvtColor(printscreen_pil, cv2.COLOR_BGR2RGB))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
