import os
import numpy as np

start = 1
file_name = 'training_data_{}.npy'.format(start)
##np_load_old = np.load
# modify the default parameters of np.load
##np.load = lambda *a,**k: np_load_old(*a, allow_pickle=True, **k)
training_data = []

while os.path.exists(file_name):
    file_data = np.load(file_name, allow_pickle = True)
    for data in file_data:
        img = data[0]
        key = data[1]
        training_data.append([img,key])
    start += 1
    file_name = 'training_data_{}.npy'.format(start)

##print(len(training_data))

def load_data():
    return (training_data)
