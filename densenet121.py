# -*- coding: utf-8 -*-
"""DenseNet121.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dJbmbcu7slX_XlkQECBG9m1DK-Fp0lcc
"""

!pip install tensorflow-gpu

img_width=224
img_height=224
train_data_dir='/content/drive/MyDrive/Datasets/chestxray/train'
valid_data_dir='/content/drive/MyDrive/Datasets/chestxray/val'

epochs=40
batch_size=32

from tensorflow.keras.applications.densenet import DenseNet121,preprocess_input
basemdldensenet=DenseNet121()
basemdldensenet.summary()

basemdldensenet=DenseNet121(weights='imagenet',input_shape=(img_width,img_height,3),include_top=False)
basemdldensenet.summary()

for lyr in basemdldensenet.layers:
  lyr.trainable=False

from tensorflow.keras import layers
from tensorflow.keras.layers import Dense,Flatten
from tensorflow.keras.models import Model

x=basemdldensenet.output
x=Dense(1024,activation='relu')(x)
x=Dense(1024,activation='relu')(x)

x=Flatten()(x)

x=Dense(512,activation='relu')(x)

x=layers.Dropout(0.5)(x)

x=Dense(2,activation='relu')(x)

mymdl=Model(basemdldensenet.input,x)

mymdl.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

import glob
numfolders=glob.glob('/content/drive/MyDrive/Datasets/chestxray/train/*')
len(numfolders)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input,
                                 rescale=1/255,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 brightness_range=(0.1,0.5),
                                 horizontal_flip=True)

val_datagen=ImageDataGenerator(rescale=1./255)

training_set=train_datagen.flow_from_directory(train_data_dir,
                                               target_size=(img_width,img_height),
                                               batch_size=batch_size,
                                               class_mode='categorical'
)

training_set.class_indices

val_set=val_datagen.flow_from_directory(valid_data_dir,
                                        target_size=(img_width,img_height),
                                        batch_size=batch_size,
                                        class_mode='categorical')

val_set.class_indices

!pip install pillow==4.0.0

mdl=mymdl.fit(training_set,
              validation_data=val_set,
              epochs=epochs,
              steps_per_epoch=len(training_set),
              validation_steps=len(val_set)
              )