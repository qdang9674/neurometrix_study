import socket 
import json 
import threading 
import matplotlib.pyplot as plt 
import matplotlib


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from scipy.signal import butter, filtfilt
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow import keras
import neurokit2 as nk
from scipy import stats
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np
from murat_ecg_library import get_ecg_features


SERVER_IP = socket.gethostbyname(socket.gethostname())  # get the server's ip 
SERVER_CONNECTION_PORT = 65430 # get the port we will be connecting from
DATA_SIZE = 20000 # how much data we should read
EXCPECTED_CONNECTIONS = 4 # how many computers will be sending data 
NUM_POINTS_TO_GRAPH = 750 # 3 seconds worth of data

# will track data from clients that connect
client_data_history = {}

ecg_scaler = StandardScaler()
# initialize StandardScaler
eye_scaler = StandardScaler()

# load saved TensorFlow model
ecg_model_path = r"C:\Users\brook\Desktop\Descartes_Real_Time_Predictions\Mural_ECG_model\model"
ecg_model = tf.saved_model.load(ecg_model_path)

eye_model_path = r"C:\Users\brook\Desktop\Descartes_Real_Time_Predictions\Quang_eye_model\model_save"
eye_model = tf.saved_model.load(eye_model_path)

def buffer_to_json(data):
    """
        The buffer can be filled with a bunch of json objects.
        This will parse through the buffer and seperate json objects 
        into a list
    """

    # creates list of dictionary like string 
    delimiter = "}" 
    data =  [json.loads(x+delimiter) for x in data.split(delimiter) if x] # creates list of json objects 
    return data 

def open_socket_handler():
    if SERVER_CONNECTION_PORT < 20000:
        print("Port given needs to be greater than 20000")
        return 
        
    print("Starting Server at {}".format(SERVER_IP))
    
    # create the socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind socket object to the actual socket it should listen from 
    server_socket.bind((SERVER_IP, SERVER_CONNECTION_PORT))
    server_socket.listen()


    while True: 
    
        # wait for a connection from a client
        client_socket, client_address = server_socket.accept()
        print("Got connection from client at {}".format(client_address))
        # service this connection 
        listen = threading.Thread(target=handle_client, args=(client_socket, client_address, ))
        listen.start()
        
        
def handle_client(client_socket, client_address):
    """
        Handles communcation 
        between server and client 

        Servicer 
    """
    try: 
        while True:
            
            # read from socket 
            data = client_socket.recv(DATA_SIZE)
            if not data:
                continue
            
            try :
                data = data.decode('utf-8') # decode byte string so we can parse it 
                
                # parse through string (should be formatted as json)
                json_data_list = buffer_to_json(data)
            except :
                print("Invalid data read, continue")
                print(data)
                print()
                continue
                
            # loop through all json entries 
            for entry in json_data_list:

                # Check who connected, and setup tracking for this computer  
                comp_name = entry["Computer_name"]

                # add computer name to dictionary so we can store all data that comes in the future  
                if comp_name not in client_data_history.keys():
                    client_data_history[comp_name] = {}
                    #physical data
                    client_data_history[comp_name]['ecg_data']  = []
                    client_data_history[comp_name]['eda_data']  = []
                    client_data_history[comp_name]['sensor_time'] = []
                    
                    client_data_history[comp_name]['Pupil_left'] = []
                    client_data_history[comp_name]['Pupil_right'] = []
                    client_data_history[comp_name]['Pupil_average'] = []
                    client_data_history[comp_name]['Gaze_X'] = []
                    client_data_history[comp_name]['Gaze_Y'] = []                    
                    client_data_history[comp_name]['eye_time'] = []
                    
                    #eye prediction
                    client_data_history[comp_name]['eye_prediction'] = []
                    
                    #ecg_prediction data
                    client_data_history[comp_name]['hr_mean'] = []
                    client_data_history[comp_name]['hr_max'] = []
                    client_data_history[comp_name]['hr_min'] = []
                    client_data_history[comp_name]['heart_rate_variability'] = []
                    client_data_history[comp_name]['snr_values'] = []
                    client_data_history[comp_name]['ecg_prediction'] = []
                    
                data_type = entry['data_type'] # Data type tells us what fields we should check for 

                if data_type == "Pupil_Data":

                    # get sent over pupil data 
                    pupil_left = entry['Pupil_left']
                    pupil_right = entry['Pupil_right']
                    pupil_average = get_pd_average(pupil_left,pupil_right)
                    
                    gaze_X = entry['Gaze_X']
                    gaze_Y = entry['Gaze_Y']
                    eye_time_data = float(entry['Timestamp'])/1000 #convert milisecond to second
                      
                    
                    # truncate old data 
                    if len(client_data_history[comp_name]['Pupil_left']) > NUM_POINTS_TO_GRAPH* 200:
                        client_data_history[comp_name]['Pupil_left']  = client_data_history[comp_name]['Pupil_left'][-NUM_POINTS_TO_GRAPH*100:]
                        client_data_history[comp_name]['Pupil_right']  = client_data_history[comp_name]['Pupil_right'][-NUM_POINTS_TO_GRAPH*100:]
                        client_data_history[comp_name]['Pupil_average']  = client_data_history[comp_name]['Pupil_average'][-NUM_POINTS_TO_GRAPH*100:]
                        client_data_history[comp_name]['Gaze_X']  = client_data_history[comp_name]['Gaze_X'][-NUM_POINTS_TO_GRAPH*100:]
                        client_data_history[comp_name]['Gaze_Y']  = client_data_history[comp_name]['Gaze_Y'][-NUM_POINTS_TO_GRAPH*100:]
                        client_data_history[comp_name]['eye_time']  = client_data_history[comp_name]['eye_time'][-NUM_POINTS_TO_GRAPH*100:]
                    
                    # add new pupil data to tracking list 
                    client_data_history[comp_name]['Pupil_left'].append(pupil_left)
                    client_data_history[comp_name]['Pupil_right'].append(pupil_right)
                    client_data_history[comp_name]['Pupil_average'].append(pupil_average)
                    client_data_history[comp_name]['Gaze_X'].append(gaze_X)
                    client_data_history[comp_name]['Gaze_Y'].append(gaze_Y)
                    client_data_history[comp_name]['eye_time'].append(eye_time_data)
                    
                    
                elif data_type == "Heart_Data":

                    # get sent over heart data 
                    ecg_data = entry['ecg_data']
                    eda_data = entry['eda_data']
                    sensor_time = float(entry['Timestamp'])
                    
                    # ensure tracking lists arent taking up too much memory. Once we have double the points we want to display, clear out old half of list 
                    if len(client_data_history[comp_name]['ecg_data']) > NUM_POINTS_TO_GRAPH* 200:
                        client_data_history[comp_name]['ecg_data']  = client_data_history[comp_name]['ecg_data'][-NUM_POINTS_TO_GRAPH*100:]
                        client_data_history[comp_name]['eda_data']  = client_data_history[comp_name]['eda_data'][-NUM_POINTS_TO_GRAPH*100:]
                        client_data_history[comp_name]['sensor_time']  = client_data_history[comp_name]['sensor_time'][-NUM_POINTS_TO_GRAPH*100:]
                        
                        
                    # add data to the tracking list 
                    client_data_history[comp_name]['ecg_data'].append(ecg_data)
                    client_data_history[comp_name]['eda_data'].append(eda_data)
                    client_data_history[comp_name]['sensor_time'].append(sensor_time)

    except KeyboardInterrupt:
        return

def plot_function():
    fig, axes = plt.subplots(nrows =EXCPECTED_CONNECTIONS  , ncols = 5, figsize=(10, 15))

    plt.ion()

    while True:
        #fig.show()
        fig.canvas.draw()

        # GO THROUGH EACH CONNECTION AND PLOT DATA        
        for i, connection in enumerate(client_data_history.keys()):
            ecg_data = client_data_history[connection]["ecg_data"][-NUM_POINTS_TO_GRAPH:]
            eda_data = client_data_history[connection]["eda_data"][-NUM_POINTS_TO_GRAPH:]
            pupil_average_data = client_data_history[connection]['Pupil_average'][-NUM_POINTS_TO_GRAPH:]
            
            #calculate ecg_prediction
            calculate_ECG_prediction(connection)
            ecg_prediction = np.array(client_data_history[connection]['ecg_prediction'][-NUM_POINTS_TO_GRAPH:])
            snr    = client_data_history[connection]['snr_values'][-NUM_POINTS_TO_GRAPH:]
            hr_mean= client_data_history[connection]['hr_mean'][-NUM_POINTS_TO_GRAPH:]
            
            #calculate eye_prediction
            calcualte_EYE_prediction(connection)
            eye_prediction = np.array(client_data_history[connection]['eye_prediction'][-NUM_POINTS_TO_GRAPH:])
            
            
            ########################
            #PLOTING               #
            ########################
            # plot ecg data
            axes[i, 0].clear()
            axes[i, 0].set_title("{} ECG".format(connection))
            axes[i, 0].plot(ecg_data)
      
            # plot Pupil Left data 
            axes[i, 1].clear()
            axes[i, 1].set_title("{} Pupil Diameter".format(connection))
            axes[i, 1].plot(pupil_average_data)

            # plot pupil data 
            axes[i, 2].clear()
            axes[i, 2].set_title("{} Hr_mean".format(connection))
            axes[i, 2].plot(hr_mean)
            
            # plot prediction array 
            x_axis_index = np.arange(len(ecg_prediction))
            axes[i, 3].clear()
            axes[i, 3].set_title("{} ECG Prediction".format(connection))
            axes[i, 3].plot(ecg_prediction, color='black')
            axes[i, 3].set_ylabel('Probability')            
            axes[i, 3].axhline(y=0.5, linestyle='--', color='red')
            axes[i, 3].set_ylim([0, 1])
            axes[i, 3].fill_between(x_axis_index, ecg_prediction, where=(ecg_prediction >= 0.5), color='red', alpha=0.3, linewidth=2.5)
                        
            # plot prediction array 
            x_axis_index = np.arange(len(eye_prediction))
            axes[i, 4].clear()
            axes[i, 4].set_title("{} Eye Prediction".format(connection))
            axes[i, 4].plot(eye_prediction, color='black')
            axes[i, 4].set_ylabel('Probability')            
            axes[i, 4].axhline(y=0.5, linestyle='--', color='red')
            axes[i, 4].set_ylim([0, 1])
            axes[i, 4].fill_between(x_axis_index, eye_prediction, where=(eye_prediction >= 0.5), color='red', alpha=0.3, linewidth=2.5)
            
        fig.canvas.draw()
        fig.tight_layout()
        plt.pause(0.1)


def calculate_ECG_prediction(comp_name):
        global client_data_history
        
        time_data = client_data_history[comp_name]['sensor_time']
        
        window_size = 30
        fs= 250
        
        if len(time_data) < window_size*fs:
            client_data_history[comp_name]['ecg_prediction'].append(np.nan)
            return
            
        # Get start and end index for current animation frame       
        ecg_window = np.array(client_data_history[comp_name]["ecg_data"][-(fs*window_size)-1:])
        time_window = np.array(time_data[-(fs*window_size)-1:])
        
        try:
            hr_mean, hr_max, hr_min, heart_rate_variability, snr_values = get_ecg_features(ecg_window[-1*window_size*fs:], time_window,fs=fs)
        except ValueError as e:
            print("Error while compute ECG heart_rate: ", e)
            client_data_history[comp_name]['ecg_prediction'].append(np.nan)
            return

        client_data_history[comp_name]['hr_mean'].append(hr_mean)
        client_data_history[comp_name]['hr_max'].append(hr_max)
        client_data_history[comp_name]['hr_min'].append(hr_min)
        client_data_history[comp_name]['heart_rate_variability'].append(heart_rate_variability)
        client_data_history[comp_name]['snr_values'].append(snr_values)

        
        hr_data = np.array([
                client_data_history[comp_name]['hr_mean'],
                client_data_history[comp_name]['hr_max'],
                client_data_history[comp_name]['hr_min'],
                client_data_history[comp_name]['snr_values']
                ])
        # Standardize the heart rate data
        hr_data_std = ecg_scaler.fit_transform(hr_data.T)
        # Get the standardized features for the current time
        current_features_std = hr_data_std[-1]
        # Make a prediction using the model
        prediction = ecg_model(current_features_std.reshape(1, -1))
        client_data_history[comp_name]['ecg_prediction'].append(prediction[0][0])
        

def calcualte_EYE_prediction(comp_name):
    global client_data_history
    limit_missing_value = 15
    cut_window = 125
    fs = 250
    
    #if length is too small, stop
    if len(client_data_history[comp_name]['Pupil_average']) < NUM_POINTS_TO_GRAPH:
        client_data_history[comp_name]['eye_prediction'].append(np.nan)
        return        
    
    #get full data for normalization
    pd_average_full = np.array(client_data_history[comp_name]['Pupil_average'])
    gaze_X_full = np.array(client_data_history[comp_name]['Gaze_X'])
    gaze_Y_full = np.array(client_data_history[comp_name]['Gaze_Y'])
    time_full = np.array(client_data_history[comp_name]['eye_time'])
    
    
    #only get the latest data for prediction
    pd_average_low_fs = pd_average_full[-cut_window:]
    gaze_X_low_fs = gaze_X_full[-cut_window:]
    gaze_Y_low_fs = gaze_Y_full[-cut_window:]
    time_low_fs = time_full[-cut_window:]
    
    
    #if too much missing data, stop
    if max_consecutive_nan(pd_average_low_fs)>= limit_missing_value\
        or max_consecutive_nan(gaze_X_low_fs)>= limit_missing_value\
        or max_consecutive_nan(gaze_Y_low_fs)>= limit_missing_value:
        
        client_data_history[comp_name]['eye_prediction'].append(np.nan)
        return
    
    
    #interpolate missing data
    mask = np.isnan(pd_average_low_fs) #missing index
    pd_average_low_fs[mask] = np.interp(time_low_fs[mask], time_low_fs[~mask], pd_average_low_fs[~mask])
    
    mask = np.isnan(gaze_X_low_fs) #missing index
    gaze_X_low_fs[mask] = np.interp(time_low_fs[mask], time_low_fs[~mask], gaze_X_low_fs[~mask])
    
    mask = np.isnan(gaze_Y_low_fs) #missing index
    gaze_Y_low_fs[mask] = np.interp(time_low_fs[mask], time_low_fs[~mask], gaze_Y_low_fs[~mask])
        
    
    #interpolate data to higher frequency
    end_time = time_low_fs[-1]
    time_high_fs = np.linspace(end_time-1,end_time,250) #get 1 second of data
    
    pd_average_high_fs = interpolate.interp1d(time_low_fs, pd_average_low_fs, kind='linear')(time_high_fs)
    gaze_X_high_fs = interpolate.interp1d(time_low_fs, gaze_X_low_fs, kind='linear')(time_high_fs)
    gaze_Y_high_fs = interpolate.interp1d(time_low_fs, gaze_Y_low_fs, kind='linear')(time_high_fs)

    #predict samples
    data_sample = np.array([pd_average_high_fs,gaze_X_high_fs,gaze_Y_high_fs]).T
    
    
    #normalization
    # remove missing data first
    pd_average_full = pd_average_full[~numpy.isnan(pd_average_full)]
    gaze_X_full = gaze_X_full[~numpy.isnan(gaze_X_full)]
    gaze_Y_full = gaze_Y_full[~numpy.isnan(gaze_Y_full)]
    
    #need to get all arrays on the equal length
    min_index_length = min(len(pd_average_full),len(gaze_X_full),len(gaze_Y_full))
    
    fit_data = np.array([ pd_average_full[-min_index_length:],gaze_X_full[-min_index_length:],gaze_Y_full[-min_index_length:] ]).T
    eye_scaler.fit(fit_data)


    data_sample_std = eye_scaler.transform(data_sample)
    prediction = eye_model(data_sample_std)
    client_data_history[comp_name]['eye_prediction'].append(prediction[0][0])
    
    

def max_consecutive_nan(arr):
    max_count = 0
    count = 0

    for value in arr:
        if np.isnan(value):
            count += 1
            max_count = max(max_count, count)
        else:
            count = 0

    return max_count

def get_pd_average(pupil_left, pupil_right):
    #pupil_left missing case
    if np.isnan(pupil_left):
        pd_average = pupil_right
    
    #pupil_right missing case
    elif np.isnan(pupil_right):
        pd_average = pupil_left
        
    else:
        pd_average = (pupil_left + pupil_right) /2
        
    return pd_average

  
def start_server():


    # handle plotting 
    socket_handler = threading.Thread(target=open_socket_handler)
    socket_handler.start()
    
    plot_function()



        

if __name__ == "__main__":
    start_server()