import numpy as np
import cv2
from PIL import ImageGrab
import time
from directinput import W, A, S, D, PressKey, ReleaseKey

for i in list(range(7))[::-1]:
    print(i+1)
    time.sleep(1)

#pressing and releasing key
print('key down')
PressKey(W)
time.sleep(3)
print('key up')
ReleaseKey(W)

def process_image(original_image):
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGRA2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=200, threshold2=300)
    return processed_image

##last_time = time.time()
##while(True):
##    screen = np.array(ImageGrab.grab(bbox=(0, 40, 800, 640)))## converting to np array here to prevent low fps caused by pil
##    edge_screen = process_image(screen)
##    printscreen_numpy = np.array(printscreen_pil.getdata(),dtype='uint8').reshape((printscreen_pil.size[1],printscreen_pil.size[0],3))
##    print('Loop took {} second'.format(time.time()-last_time))
##    cv2.imshow('window1',cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
##    cv2.imshow('window2', edge_screen)
##    if cv2.waitKey(25) & 0xFF == ord('q'):
##        break
