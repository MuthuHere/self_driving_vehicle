import numpy as np
import time as time
import os
from datetime import datetime
from random import shuffle
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.layers import Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam

def setup():
    tf.compat.v1.keras.backend.clear_session()
    config = tf.compat.v1.ConfigProto()
    config.gpu_options.allow_growth = True
    config.log_device_placement = True
    sess = tf.compat.v1.Session(config=config)
    tf.compat.v1.keras.backend.set_session(sess)

setup()

log_dir = os.path.join("logs","scalars","vgg16_model",)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir,histogram_freq=1,write_images=True)

LAST_RUN = 1583693488
epochs = 30
files = 149
v = int(time.time())
WIDTH = 480
HEIGHT = 270
MODEL_NAME = 'model_gta_vgg16_v-{}.h5'.format(v)
PREV_MODEL_NAME = 'model_gta_vgg16_v-{}.h5'.format(LAST_RUN)

for e in range(epochs):
    setup()
    model = load_model(PREV_MODEL_NAME)
    #model.compile(Adam(lr=0.001),loss='categorical_crossentropy',metrics=['accuracy'])
    data_order = [i for i in range(1,files+1)]
    shuffle(data_order)
    for count,i in enumerate(data_order):
        print(count)
        print(i)
        file_name = 'training_data_{}.npy'.format(i)
        train_data = np.load(file_name,allow_pickle=True)
        train_set = train_data[:-100]
        test_set = train_data[-100:]
        X = np.array([i[0] for i in train_set]).reshape(-1,WIDTH,HEIGHT,3)
        Y = np.array([i[1] for i in train_set])
        test_x = np.array([i[0] for i in test_set]).reshape(-1,WIDTH,HEIGHT,3)
        test_y = np.array([i[1] for i in test_set])
        model.fit(X,Y,batch_size=8,epochs=1,validation_data=(test_x,test_y),callbacks=[tensorboard_callback],shuffle=True)
    model.save(MODEL_NAME)
    LAST_RUN = v
    v = int(time.time())
    MODEL_NAME = 'model_gta_vgg16_v-{}.h5'.format(v)
    PREV_MODEL_NAME = 'model_gta_vgg16_v-{}.h5'.format(LAST_RUN)