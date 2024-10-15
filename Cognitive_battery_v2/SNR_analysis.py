#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#get_ipython().system('jupyter nbconvert --to script SNR_analysis.ipynb')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn_extra.cluster import KMedoids
from sklearn.metrics import silhouette_score
from scipy.spatial import ConvexHull
from scipy.interpolate import interp1d
from sklearn.metrics import pairwise_distances# Load your DataFrame (result_df) if you haven't already


import neurokit2 as nk
from scipy.signal import butter, filtfilt
from scipy import stats


import numpy as np


# In[2]:


def get_ecg_features(ecg, time_in_sec, fs):
    """
    Compute ECG features from raw ECG signal.

    Parameters
    ----------
    ecg : array-like
        Raw ECG signal.
    time_in_sec : array-like
        Timestamps corresponding to each sample of the ECG signal.
    fs : float
        Sampling frequency of the ECG signal.

    Returns
    -------
    array
        Array of ECG features: [mean heart rate, maximum heart rate, minimum heart rate, heart rate variability].
    """
    try:
        b, a = butter(4, (0.25, 25), 'bandpass', fs=fs)
        ecg_filt = filtfilt(b, a, ecg, axis=0)
        ecg_cleaned = nk.ecg_clean(ecg_filt, sampling_rate=fs)
        instant_peaks, rpeaks = nk.ecg_peaks(ecg_cleaned, sampling_rate=fs,method="engzeemod2012")
    except Exception as e:
        raise ValueError("Error processing ECG signal: " + str(e))

    rr_times = time_in_sec[rpeaks['ECG_R_Peaks']]
    if len(rr_times) == 0:
        raise ValueError("No R-peaks detected in ECG signal.")
    
    # Assuming d_rr contains the time intervals between successive heartbeats in seconds
    d_rr = np.diff(rr_times)
    heart_rate = 60 / d_rr
    if heart_rate.size == 0:
        raise ValueError("Error computing heart rate from ECG signal.")
    
    valid_heart_rate = heart_rate[~np.isnan(heart_rate)]
    z_scores = np.abs(stats.zscore(valid_heart_rate))

    # Define a z-score threshold beyond which a value is considered an outlier
    z_score_threshold = 4.0

    # Remove outliers from the valid_heart_rate array
    heart_rate = valid_heart_rate[z_scores <= z_score_threshold]

    hr_mean = np.nanmean(heart_rate)
    hr_min = np.nanmin(heart_rate)
    hr_max = np.nanmax(heart_rate)
    d_rr_ms = 1000 * d_rr
    d_d_rr_ms = np.diff(d_rr_ms)

    valid_d_d_rr_ms = d_d_rr_ms[~np.isnan(d_d_rr_ms)] 
    z_scores = np.abs(stats.zscore(valid_d_d_rr_ms))
    d_d_rr_ms= valid_d_d_rr_ms[z_scores <= z_score_threshold]
    heart_rate_variability = np.sqrt(np.nanmean(np.square(d_d_rr_ms)))

    # Create a new signal 'ecg_with_rr_intervals' with RR intervals and a 1-second window around each RR interval
    ecg_with_rr_intervals = []
    ecg_with_rr_intervals_cleaned = []

    for rr_interval in rr_times:
        start_time = rr_interval - 0.1 # 1 second before the RR interval
        end_time = rr_interval + 0.1   # 1 second after the RR interval
        indices = np.where((time_in_sec >= start_time) & (time_in_sec <= end_time))[0]

        # Validate indices to ensure they are within bounds
        indices = indices[(indices >= 0) & (indices < len(ecg))]

        if len(indices) > 0:
            ecg_with_rr_intervals.extend(ecg[indices])
            ecg_with_rr_intervals_cleaned.extend(ecg_cleaned[indices])

    # Convert lists to NumPy arrays
    ecg_with_rr_intervals = np.array(ecg_with_rr_intervals)
    ecg_with_rr_intervals_cleaned = np.array(ecg_with_rr_intervals_cleaned)

    # Calculate noise power (mean squared amplitude of noise)
    signal_power = np.var(ecg_with_rr_intervals)
    noise_power = np.var(ecg_with_rr_intervals - ecg_with_rr_intervals_cleaned)

    # Calculate noise power (mean squared amplitude of noise)
    #signal_power = np.var(ecg)
    #noise_power = np.var(ecg - ecg_cleaned)

     # Calculate SNR in dB and append it to the array
    snr_values = 10 * np.log10(signal_power / noise_power)
    
    return hr_mean, hr_max, hr_min, heart_rate_variability, snr_values


# In[3]:


ECG_FEATURES_LIST = 'ecg_data'

# data is pandas.DataFrame
# ml_model should have predict method
def ecg_online_prediction(data,ml_model,begin = 0, predict_interval = 250, features = ECG_FEATURES_LIST):
    cutoff_db_snr = 4 
    cutoff_hr_mean = 180
    cutoff_hr_variability = 250
    fs = 250
    
    samples_list = []
    online_predict = []
    end = begin + (250 * 30)
    

    
    #standardlizing
    samples_list = np.array(samples_list)
    if len(samples_list) == 0:
        return samples_list
        
    ecg_scaler = StandardScaler()
    samples_list_scaled = ecg_scaler.fit_transform(samples_list)
    # predicting
    online_predict = ml_model(samples_list_scaled)
    
    return np.array(online_predict)


# In[4]:


DATA_DIR = r'/nfs/ada/jbrook1/users/qdang1/Descartes/Cognitive_battery/'
df_ecg = pd.read_pickle(DATA_DIR + "df_sensor.pkl")
df_ecg


# In[ ]:


predict_interval = 250
fs = 250
hr_mean_list = []
hr_max_list = []
hr_min_list = []
hrv_list = []
snr_list = []

for index, row in df_ecg.iterrows():
    current_df = pd.DataFrame(row).T
    print(index, ": ", current_df.shape)
    
    temp_df = current_df['data'].apply(lambda x: pd.Series(x))
    current_df = pd.concat([current_df.drop('data', axis=1), temp_df.drop('eda_data',axis=1)], axis=1)
    current_df = current_df.explode(['Timestamp','ecg_data'])
    current_df = current_df.astype({'Timestamp':'float64','ecg_data': 'float64'})
    
    if current_df.shape[0] == 0:
        continue

    # #interpolation
    temp_df = current_df[['Timestamp','ecg_data']]
    temp_df = temp_df.set_index(pd.to_datetime(temp_df['Timestamp'], unit='s'))
    temp_df = temp_df.interpolate(method='time',limit = 10)
    current_df[['ecg_data']] = np.array(temp_df[['ecg_data']])


    #generate feature
    begin = 0 
    end = begin + (250 * 30)    
    while begin < (len(current_df) - (250* 30) ):
        temp_ecg = np.array(current_df.iloc[begin:end]['ecg_data'])
        temp_time = np.array(current_df.iloc[begin:end]['Timestamp'])
        
        #filter nan
        if np.isnan(temp_ecg).sum() > 0 or np.isnan(temp_time).sum() > 0:
            begin += predict_interval 
            end = begin + (250 * 30)
            continue
            
        #get ecg feature
        try:
            hr_mean, hr_max, hr_min, heart_rate_variability, snr_values = get_ecg_features(temp_ecg, temp_time,fs=fs)
        except ValueError as e:
            begin += predict_interval 
            end = begin + (250 * 30)
            continue


        hr_mean_list.append(hr_mean)
        hr_max_list.append(hr_max)
        hr_min_list.append(hr_min)
        hrv_list.append(heart_rate_variability)
        snr_list.append(snr_values)
        
        begin += predict_interval 
        end = begin + (250 * 30)

hr_mean_list = np.array(hr_mean_list)
hr_max_list = np.array(hr_max_list)
hr_min_list = np.array(hr_min_list)
hrv_list = np.array(hrv_list)
snr_list = np.array(snr_list)


# In[ ]:


np.save('hr_mean_list.npy', hr_mean_list)
np.save('hr_max_list.npy', hr_max_list)
np.save('hr_min_list.npy', hr_min_list)
np.save('hr_hrv_list.npy', hrv_list)
np.save('hr_snr_list.npy', snr_list)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




