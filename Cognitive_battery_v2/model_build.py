#!/usr/bin/env python
# coding: utf-8

# # Import

# In[54]:


#!jupyter nbconvert --to script model_build.ipynb

import csv
import json
import pywt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import neurokit2 as nk
from scipy.signal import butter, filtfilt
from scipy.signal import resample
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.stats import pearsonr, spearmanr, linregress
from sklearn.preprocessing import StandardScaler
import random
import tensorflow as tf
from tqdm.notebook import tqdm
from tensorflow.python.client import device_lib
import matplotlib.colors as mcolors
import random

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, f1_score, accuracy_score, matthews_corrcoef


# In[2]:


print(tf.__version__)


# In[3]:


tf.config.experimental.list_physical_devices('GPU')
device_lib.list_local_devices()


# In[70]:


MODEL_NAME = 'baseline_merge'
RUN = 'run11_' + MODEL_NAME+ '/'

CURRENT_DIR = os.getcwd()
DATA_DIR = CURRENT_DIR + '/data/'
MASTER_OUTPUT_DIR = CURRENT_DIR + '/output/'
OUTPUT_DIR = MASTER_OUTPUT_DIR + RUN
print(DATA_DIR)
print(OUTPUT_DIR)


# In[71]:


os.makedirs(OUTPUT_DIR, exist_ok=True)


# # Load_data

# In[6]:


# Initialize an empty list to store the arrays
X_dict = {}
Y_dict = {}

# Load each file and append the array to the list
for i in range(5):
    X_filename = f'X_fold{i}.npy'
    X_dict[i] = np.load(DATA_DIR + X_filename, allow_pickle=True)

    Y_filename = f'Y_fold{i}.npy'
    Y_dict[i] = np.load(DATA_DIR + Y_filename,  allow_pickle=True)

for i in range(5):
    print(f'i: {i}, X: {X_dict[i].shape}, Y: {Y_dict[i].shape}')


# In[7]:


for index in range(1):
    train_list = [0, 1, 2, 3, 4]
    train_list.remove(index)
    test_list = [index]

    print(f'train: {train_list}, test: {test_list}')

    X_train = X_dict[train_list[0]]
    Y_train = Y_dict[train_list[0]]
    X_test =  X_dict[test_list[0]]
    Y_test =  Y_dict[test_list[0]]
    
    for i_train in train_list[1:]:
        X_train = np.concatenate([X_train,X_dict[i_train] ],axis = 0)
        Y_train = np.concatenate([Y_train,Y_dict[i_train] ],axis = 0)

    for i_test in test_list[1:]:
        X_test = np.concatenate([X_test,X_dict[i_test] ],axis = 0)
        Y_test = np.concatenate([Y_test,Y_dict[i_test] ],axis = 0)

    print(f'X_train: {X_train.shape}, Y_train: {Y_train.shape}, X_test : {X_test.shape}, Y_test: {Y_test.shape}')


# In[8]:


X_train_demo          = np.array(X_train[:,0].tolist()).squeeze(1)
X_train_1_eye         = np.array(X_train[:,1].tolist())
X_train_1_eye_wavelet = np.array(X_train[:,2].tolist())
X_train_1_ecg         = np.array(X_train[:,3].tolist())
X_train_1_ecg_feature = np.array(X_train[:,4].tolist())
X_train_2_eye         = np.array(X_train[:,5].tolist())
X_train_2_ecg         = np.array(X_train[:,6].tolist())
X_train_2_ecg_feature = np.array(X_train[:,7].tolist())




# In[9]:


#cliping with 99.5.5% 

X_train_1_eye = np.clip(X_train_1_eye, np.percentile(X_train_1_eye, 0.5), np.percentile(X_train_1_eye, 99.5))
X_train_1_eye_wavelet = np.clip(X_train_1_eye_wavelet, np.percentile(X_train_1_eye_wavelet, 0.5), np.percentile(X_train_1_eye_wavelet, 99.5))
X_train_1_ecg = np.clip(X_train_1_ecg, np.percentile(X_train_1_ecg, 2.5), np.percentile(X_train_1_ecg, 97.5))
X_train_1_ecg_feature = np.clip(X_train_1_ecg_feature, np.percentile(X_train_1_ecg_feature, 2.5), np.percentile(X_train_1_ecg_feature, 97.5))
X_train_2_eye = np.clip(X_train_2_eye, np.percentile(X_train_2_eye, 0.5), np.percentile(X_train_2_eye, 99.5))
#X_train_2_eye_wavelet = np.clip(X_train_2_eye_wavelet, np.percentile(X_train_2_eye_wavelet, 0.5), np.percentile(X_train_2_eye_wavelet, 99.5))
X_train_2_ecg = np.clip(X_train_2_ecg, np.percentile(X_train_2_ecg, 2.5), np.percentile(X_train_2_ecg, 97.5))
X_train_2_ecg_feature = np.clip(X_train_2_ecg_feature, np.percentile(X_train_2_ecg_feature, 2.5), np.percentile(X_train_2_ecg_feature, 97.5))

print(f'demo:          {X_train_demo.shape}\n\
eye_1:         {X_train_1_eye.shape}\neye_1_wavelet: {X_train_1_eye_wavelet.shape}\n\
ecg_1:         {X_train_1_ecg.shape}\necg_1_feature: {X_train_1_ecg_feature.shape}\n\
eye_2:         {X_train_2_eye.shape}\n\
ecg_2:         {X_train_2_ecg.shape}\necg_2_feature: {X_train_2_ecg_feature.shape}\n')


# In[10]:


X_test_demo          = np.array(X_test[:,0].tolist()).squeeze(1)
X_test_1_eye         = np.array(X_test[:,1].tolist())
X_test_1_eye_wavelet = np.array(X_test[:,2].tolist())
X_test_1_ecg         = np.array(X_test[:,3].tolist())
X_test_1_ecg_feature = np.array(X_test[:,4].tolist())
X_test_2_eye         = np.array(X_test[:,5].tolist())
X_test_2_ecg         = np.array(X_test[:,6].tolist())
X_test_2_ecg_feature = np.array(X_test[:,7].tolist())




# In[11]:


#cliping with 99.5% 

X_test_1_eye = np.clip(X_test_1_eye, np.percentile(X_test_1_eye, 0.5), np.percentile(X_test_1_eye, 99.5))
X_test_1_eye_wavelet = np.clip(X_test_1_eye_wavelet, np.percentile(X_test_1_eye_wavelet, 0.5), np.percentile(X_test_1_eye_wavelet, 99.5))
X_test_1_ecg = np.clip(X_test_1_ecg, np.percentile(X_test_1_ecg, 2.5), np.percentile(X_test_1_ecg, 97.5))
X_test_1_ecg_feature = np.clip(X_test_1_ecg_feature, np.percentile(X_test_1_ecg_feature, 2.5), np.percentile(X_test_1_ecg_feature, 97.5))
X_test_2_eye = np.clip(X_test_2_eye, np.percentile(X_test_2_eye, 0.5), np.percentile(X_test_2_eye, 99.5))
#X_test_2_eye_wavelet = np.clip(X_test_2_eye_wavelet, np.percentile(X_test_2_eye_wavelet, 0.5), np.percentile(X_test_2_eye_wavelet, 99.5))
X_test_2_ecg = np.clip(X_test_2_ecg, np.percentile(X_test_2_ecg, 2.5), np.percentile(X_test_2_ecg, 97.5))
X_test_2_ecg_feature = np.clip(X_test_2_ecg_feature, np.percentile(X_test_2_ecg_feature, 2.5), np.percentile(X_test_2_ecg_feature, 97.5))




print(f'demo:          {X_test_demo.shape}\n\
eye_1:         {X_test_1_eye.shape}\neye_1_wavelet: {X_test_1_eye_wavelet.shape}\n\
ecg_1:         {X_test_1_ecg.shape}\necg_1_feature: {X_test_1_ecg_feature.shape}\n\
eye_2:         {X_test_2_eye.shape}\n\
ecg_2:         {X_test_2_ecg.shape}\necg_2_feature: {X_test_2_ecg_feature.shape}\n')


# In[12]:


Y_train_dif         = np.array(Y_train[:,0].tolist())
Y_train_acc         = np.array(Y_train[:,1].tolist())



print(f'Difficulty:       {Y_train_dif.shape}\nAccuracy:         {Y_train_acc.shape}')


# In[13]:


Y_test_dif         = np.array(Y_test[:,0].tolist())
Y_test_acc         = np.array(Y_test[:,1].tolist())



print(f'Difficulty:       {Y_test_dif.shape}\nAccuracy:         {Y_test_acc.shape}')


# In[14]:


EPOCHS = 200
BATCH_SIZE = 32
PATIENCE = 20


# # Merge model

# In[21]:


print(f'demo:          {X_train_demo.shape}\n\
eye_1:         {X_train_1_eye.shape}\neye_1_wavelet: {X_train_1_eye_wavelet.shape}\n\
ecg_1:         {X_train_1_ecg.shape}\necg_1_feature: {X_train_1_ecg_feature.shape}\n\
eye_2:         {X_train_2_eye.shape}\n\
ecg_2:         {X_train_2_ecg.shape}\necg_2_feature: {X_train_2_ecg_feature.shape}\n')


# In[22]:


print(np.isnan([X_train_demo]).any())
print(np.isinf([X_train_demo]).any())
print(np.isnan([X_train_1_eye]).any())
print(np.isinf([X_train_1_eye]).any())
print(np.isnan([X_train_1_eye_wavelet]).any())
print(np.isinf([X_train_1_eye_wavelet]).any())
print(np.isnan([X_train_1_ecg]).any())
print(np.isinf([X_train_1_ecg]).any())
print(np.isnan([X_train_1_ecg_feature]).any())
print(np.isinf([X_train_1_ecg_feature]).any())

print(np.isnan([X_train_2_eye]).any())
print(np.isinf([X_train_2_eye]).any())
print(np.isnan([X_train_2_ecg]).any())
print(np.isinf([X_train_2_ecg]).any())
print(np.isnan([X_train_2_ecg_feature]).any())
print(np.isinf([X_train_2_ecg_feature]).any())



def custom_CNN_layer(input_layer, start_neuron = 16, kernel_size=9, strides_size=1, max_pool_size=5, dropout=0.3, padding='valid'):
    cnn_layer = tf.keras.layers.Conv1D(start_neuron, kernel_size, strides=strides_size,  padding=padding, activation=tf.keras.layers.LeakyReLU(),kernel_regularizer=tf.keras.regularizers.l2(0.01))(input_layer)
    cnn_layer = tf.keras.layers.Conv1D(start_neuron, kernel_size, strides=strides_size,  padding=padding, activation=tf.keras.layers.LeakyReLU(),kernel_regularizer=tf.keras.regularizers.l2(0.01))(cnn_layer)
    cnn_layer = tf.keras.layers.MaxPool1D(max_pool_size,  padding=padding)(cnn_layer)
    cnn_layer = tf.keras.layers.BatchNormalization()(cnn_layer)
    cnn_layer = tf.keras.layers.Dropout(dropout)(cnn_layer)
    return cnn_layer


# In[75]:


#create model
def baseline_merge(shape, start_neuron = 16, kernel_size_1 = 5, kernel_size_2 = 3 , strides_size=1, max_pool_size_1 = 3, max_pool_size_2 = 2 , dropout=0.3, padding='valid'):    

    input_demo                 = tf.keras.Input((shape[1],), name='input_demo') 
    input_baseline_eye         = tf.keras.Input((shape[3], shape[4]), name='input_baseline_eye') 
    input_baseline_wavelet     = tf.keras.Input((shape[6], shape[7]), name='input_baseline_eye_wavelet') 
    input_baseline_ecg         = tf.keras.Input((shape[9], shape[10]), name='input_baseline_ecg')
    input_baseline_ecg_feature = tf.keras.Input((shape[12],), name='input_baseline_ecg_feature')
    
    input_sample_eye  = tf.keras.Input((shape[14], shape[15]), name='input_sample_eye') 
    input_sample_ecg = tf.keras.Input((shape[17], shape[18]), name='input_sample_ecg')
    input_sample_ecg_feature = tf.keras.Input((shape[20],), name='input_sample_ecg_feature')


    
    #baseline eye
    baseline_eye = custom_CNN_layer(input_baseline_eye, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_eye = custom_CNN_layer(baseline_eye, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_eye = custom_CNN_layer(baseline_eye, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_eye = custom_CNN_layer(baseline_eye, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_eye = custom_CNN_layer(baseline_eye, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)

    baseline_eye = custom_CNN_layer(baseline_eye, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_eye = custom_CNN_layer(baseline_eye, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_eye = custom_CNN_layer(baseline_eye, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_eye = custom_CNN_layer(baseline_eye, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_eye = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron * 2, return_sequences=True))(baseline_eye)
    baseline_eye = tf.keras.layers.Dropout(dropout)(baseline_eye)
    baseline_eye = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron * 2, return_sequences=True))(baseline_eye)
    baseline_eye = tf.keras.layers.Dropout(dropout)(baseline_eye)
    baseline_eye = tf.keras.layers.Flatten()(baseline_eye)
    baseline_eye = tf.keras.layers.Dense(start_neuron * 4)(baseline_eye)

    #baseline eye_wavelet
    baseline_eye_wavelet = custom_CNN_layer(input_baseline_wavelet, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_eye_wavelet = custom_CNN_layer(baseline_eye_wavelet, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_eye_wavelet = custom_CNN_layer(baseline_eye_wavelet, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_eye_wavelet = custom_CNN_layer(baseline_eye_wavelet, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_eye_wavelet = custom_CNN_layer(baseline_eye_wavelet, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)

    baseline_eye_wavelet = custom_CNN_layer(baseline_eye_wavelet, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_eye_wavelet = custom_CNN_layer(baseline_eye_wavelet, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_eye_wavelet = custom_CNN_layer(baseline_eye_wavelet, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_eye_wavelet = custom_CNN_layer(baseline_eye_wavelet, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_eye_wavelet = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron * 2, return_sequences=True))(baseline_eye_wavelet)
    baseline_eye_wavelet = tf.keras.layers.Dropout(dropout)(baseline_eye_wavelet)
    baseline_eye_wavelet = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron * 2, return_sequences=True))(baseline_eye_wavelet)
    baseline_eye_wavelet = tf.keras.layers.Dropout(dropout)(baseline_eye_wavelet)
    baseline_eye_wavelet = tf.keras.layers.Flatten()(baseline_eye_wavelet)
    baseline_eye_wavelet = tf.keras.layers.Dense(start_neuron * 4)(baseline_eye_wavelet)
    
    # Baseline
    baseline_ecg = custom_CNN_layer(input_baseline_ecg, start_neuron, kernel_size=kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_ecg = custom_CNN_layer(baseline_ecg, start_neuron , kernel_size=kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_ecg = custom_CNN_layer(baseline_ecg, start_neuron , kernel_size=kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    baseline_ecg = custom_CNN_layer(baseline_ecg, start_neuron * 2, kernel_size=kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_ecg = custom_CNN_layer(baseline_ecg, start_neuron * 2, kernel_size=kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    baseline_ecg = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron, return_sequences=True))(baseline_ecg)
    baseline_ecg = tf.keras.layers.Dropout(dropout)(baseline_ecg)
    baseline_ecg = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron, return_sequences=True))(baseline_ecg)
    baseline_ecg = tf.keras.layers.Dropout(dropout)(baseline_ecg)
    baseline_ecg = tf.keras.layers.Flatten()(baseline_ecg)
    baseline_ecg = tf.keras.layers.Dense(start_neuron * 4)(baseline_ecg)
  
    
    #samples_eye
    sample_eye  = custom_CNN_layer(input_sample_eye, start_neuron, kernel_size = kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    sample_eye  = custom_CNN_layer(sample_eye, start_neuron , kernel_size =  kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    sample_eye  = custom_CNN_layer(sample_eye, start_neuron , kernel_size =  kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    sample_eye  = custom_CNN_layer(sample_eye, start_neuron * 2, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    sample_eye  = custom_CNN_layer(sample_eye, start_neuron * 4, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    sample_eye  = custom_CNN_layer(sample_eye, start_neuron * 4, kernel_size = kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    sample_eye = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron * 2, return_sequences=True))(sample_eye)
    sample_eye = tf.keras.layers.Dropout(dropout)(sample_eye)
    sample_eye = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron * 2, return_sequences=True))(sample_eye)
    sample_eye = tf.keras.layers.Dropout(dropout)(sample_eye)
    sample_eye = tf.keras.layers.Flatten()(sample_eye)
    sample_eye = tf.keras.layers.Dense(start_neuron * 8)(sample_eye)
    

    # Samples_ecg
    sample_ecg = custom_CNN_layer(input_sample_ecg, start_neuron, kernel_size=kernel_size_1, strides_size=strides_size, max_pool_size=max_pool_size_1, dropout=dropout, padding=padding)
    sample_ecg = custom_CNN_layer(sample_ecg, start_neuron * 2, kernel_size=kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    #sample_ecg = custom_CNN_layer(sample_ecg, start_neuron * 2, kernel_size=kernel_size_2, strides_size=strides_size, max_pool_size=max_pool_size_2, dropout=dropout, padding=padding)
    sample_ecg = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron * 2, return_sequences=True))(sample_ecg)
    sample_ecg = tf.keras.layers.Dropout(dropout)(sample_ecg)
    sample_ecg = tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(start_neuron * 2, return_sequences=True))(sample_ecg)
    sample_ecg = tf.keras.layers.Dropout(dropout)(sample_ecg)
    sample_ecg = tf.keras.layers.Flatten()(sample_ecg)
    sample_ecg = tf.keras.layers.Dense(start_neuron * 4)(sample_ecg)


    
    concat_layer = tf.keras.layers.Concatenate()([baseline_eye, baseline_eye_wavelet, baseline_ecg, sample_eye,sample_ecg, input_demo, input_baseline_ecg_feature, input_sample_ecg_feature])
    output_layer = tf.keras.layers.Dense(start_neuron*4,activation=tf.keras.layers.LeakyReLU())(concat_layer)
    output_layer = tf.keras.layers.Dropout(dropout)(output_layer)
    output_layer = tf.keras.layers.Dense(start_neuron*8,activation=tf.keras.layers.LeakyReLU())(output_layer)
    output_layer = tf.keras.layers.Dropout(dropout)(output_layer)
    output_0 = tf.keras.layers.Dense(3, activation='softmax', name='difficulty')(output_layer)

    
    model = tf.keras.Model(inputs=[input_demo, input_baseline_eye, input_baseline_wavelet, input_baseline_ecg, input_baseline_ecg_feature,\
                                   input_sample_eye, input_sample_ecg, input_sample_ecg_feature], outputs=[output_0])
    
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model


# In[76]:


current_shape = X_train_demo.shape + X_train_1_eye.shape + X_train_1_eye_wavelet.shape + X_train_1_ecg.shape + X_train_1_ecg_feature.shape \
+ X_train_2_eye.shape + X_train_2_ecg.shape + X_train_2_ecg_feature.shape

current_shape


# # Grid seach

# In[68]:


dict_seach = {
    'start_neuron'    : [16],
    'kernel_size_1'   : [3,5,7],
    'kernel_size_2'   : [3,5,7],
    'strides_size'    : [1,2,3],
    'max_pool_size_1' : [2,3,5],
    'max_pool_size_2' : [2,3,5],
    'dropout'         : [0.2,0.3,0.4],
    'padding'         : ['same','valid']
}



# In[ ]:


i = 0
for start_neuron in dict_seach['start_neuron']:
    for kernel_size_1 in dict_seach['kernel_size_1']:
        for kernel_size_2 in dict_seach['kernel_size_2']:
            for strides_size in dict_seach['strides_size']:
                for max_pool_size_1 in dict_seach['max_pool_size_1']:
                    for max_pool_size_2 in dict_seach['max_pool_size_2']:
                        for dropout in dict_seach['dropout']:
                            for padding in dict_seach['padding']:
                                title = f'{i}_{start_neuron}_{kernel_size_1}_{kernel_size_2}_{strides_size}_{max_pool_size_1}_{max_pool_size_2}_{dropout}_{padding}'
                                print(title)

                                reduce_LR_On_Plateau = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss',factor=0.5,patience=PATIENCE//2,verbose=1, min_delta=0.00001,)
                                early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=PATIENCE, restore_best_weights = True, mode = 'min')

                                try:
                                    model_merge = baseline_merge(current_shape, start_neuron=start_neuron, kernel_size_1 = kernel_size_1, kernel_size_2 = kernel_size_2 , strides_size= strides_size, max_pool_size_1 = max_pool_size_1, max_pool_size_2 = max_pool_size_2 , dropout=dropout, padding=padding)
                                    #model_merge.summary()
                                    
                                    history = model_merge.fit([X_train_demo, X_train_1_eye, X_train_1_eye_wavelet, X_train_1_ecg, X_train_1_ecg_feature,\
                                                             X_train_2_eye,X_train_2_ecg, X_train_2_ecg_feature], [Y_train_dif], 
                                                        epochs=EPOCHS, batch_size=BATCH_SIZE,verbose=0, shuffle=True, validation_split = 0.2, callbacks=[reduce_LR_On_Plateau,early_stopping])
                                except:
                                    print('Error, continue')
                                    i += 1
                                    continue

                                Y_pred = model_merge.predict([X_test_demo, X_test_1_eye, X_test_1_eye_wavelet, X_test_1_ecg, X_test_1_ecg_feature,\
                                                         X_test_2_eye,X_test_2_ecg, X_test_2_ecg_feature])
                                
                                # Calculate the confusion matrix
                                cm = confusion_matrix(Y_test_dif, np.argmax(Y_pred,axis=1))
                                f1 = f1_score(Y_test_dif,  np.argmax(Y_pred,axis=1), average='weighted')
                                accuracy = accuracy_score(Y_test_dif,  np.argmax(Y_pred,axis=1))
                                mcc = matthews_corrcoef(Y_test_dif,  np.argmax(Y_pred,axis=1))
                                # Display the confusion matrix using Matplotlib
                                disp = ConfusionMatrixDisplay(confusion_matrix=cm)
                                disp.plot(cmap=plt.cm.Blues)
                                plt.title(f"Confusion Matrix for {title}\nF1 Score: {f1:.2f}, MCC: {mcc:.2f}, Accuracy: {accuracy:.2f}")
                                
                                plt.savefig(OUTPUT_DIR + 'Confusion_Matrix_' + title + '.png')
                                plt.close()
                                
                                i += 1


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




