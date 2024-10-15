import numpy as np
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

# initialize StandardScaler
scaler = StandardScaler()

# load saved TensorFlow model
model_path = "/Users/muratkucukosmanoglu/Desktop/ECG-WORKS-2023/HID/model"
model = tf.saved_model.load(model_path)

# example input data with one sample
#input_data = np.array([0.5, 0.5, 0.5, -2])

# reshape input data to match expected shape
#input_data = input_data.reshape(1, -1)

# make prediction with the model
#predictions = model(input_data)
#print(predictions)


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
        b, a = butter(4, (0.5, 30), 'bandpass', fs=fs)
        ecg_filt = filtfilt(b, a, ecg, axis=0)
        ecg_cleaned = nk.ecg_clean(ecg_filt, sampling_rate=fs)
        instant_peaks, rpeaks = nk.ecg_peaks(ecg_cleaned, sampling_rate=fs)
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
    z_score_threshold = 2.0

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

    return np.array([hr_mean, hr_max, hr_min, heart_rate_variability])



ecg_signal = []
t = []
t2 = []
t3 = []
hr_mean = []
hr_max = []
hr_min = []
heart_rate_variability = []
t11= [] 
hr_features = []
predictions = []
frame_count = 0  # Initialize frame count


# Define animation function
def animate(i):
    global ecg_signal, t, hr_mean, hr_max, hr_min, heart_rate_variability, t2, t3, predictions, frame_count

    # Check if 200 frames have been processed
    if frame_count >= 200:
        return
    
    # Set sampling rate and duration
    fs = 250
    duration = 10  # seconds
    t += list(np.arange(i, i+duration, 1/fs))
    #t11 = np.arange(i, i+10000, 1/fs)

    # Compute ECG features
    window_shift = 1
    window_size = 30
    
    ecg_signal += list(nk.ecg_simulate(duration, sampling_rate=fs, heart_rate=70, noise=0.25)) # Real Time DATA

    # Get start and end index for current animation frame
    start_idx = int(i*window_shift*fs)
    end_idx = start_idx + window_size*fs

    #axs[0].clear()
    axs[0].plot(t[-window_shift*fs:], ecg_signal[-window_shift*fs:], color='black')
    #axs[0].plot(t11[-duration*window_size*fs:], ecg_signal[-duration*window_size*fs:], color='black')
    axs[0].set_title('ECG Signal')
    axs[0].set_xlabel('Time (s)')
    axs[0].set_ylabel('Amplitude (mV)')


    if t[-1]>=30:

        hr_mean += [get_ecg_features(ecg_signal[-1*window_size*fs:], np.arange(start_idx, end_idx)/fs,fs=fs)[0]]
        hr_max += [get_ecg_features(ecg_signal[-1*window_size*fs:], np.arange(start_idx, end_idx)/fs,fs=fs)[1]]
        hr_min += [get_ecg_features(ecg_signal[-1*window_size*fs:], np.arange(start_idx, end_idx)/fs,fs=fs)[2]]
        heart_rate_variability += [get_ecg_features(ecg_signal[-1*window_size*fs:], np.arange(start_idx, end_idx)/fs,fs=fs)[3]]

        #hr_min = process_ecg(ecg_signal, window_size, window_shift, fs)[0,1]
        #hr_max = process_ecg(ecg_signal, window_size, window_shift, fs)[0,2]
        #hr_variability = process_ecg(ecg_signal,window_size,window_shift,fs)[0,3]
        t2 += [np.round(np.max(t))]
        # Plot HR Mean for current frame
        #axs[1].clear()
        axs[1].plot(t2, hr_mean, color='blue')
        axs[1].set_title('HR Mean')
        axs[1].set_xlabel('Time (s)')
        axs[1].set_ylabel('HR Mean (BPM)')  

        axs[2].plot(t2, hr_max, color='red')
        axs[2].set_title('HR Max')
        axs[2].set_xlabel('Time (s)')
        axs[2].set_ylabel('HR Max (BPM)')  

        axs[3].plot(t2, hr_min, color='green')
        axs[3].set_title('HR Min')
        axs[3].set_xlabel('Time (s)')
        axs[3].set_ylabel('HR Min (BPM)')  

        axs[4].plot(t2, heart_rate_variability, color='black')
        axs[4].set_title('HR Variability')
        axs[4].set_xlabel('Time (s)')
        axs[4].set_ylabel('HR Variability (BPM)')  

        if len(hr_mean) >= 30:
            hr_data = np.array([hr_mean, hr_max, hr_min, heart_rate_variability])
            # Standardize the heart rate data
            hr_data_std = scaler.fit_transform(hr_data.T)
            t3.append(np.round(np.max(t2)))
            # Get the standardized features for the current time
            current_features_std = hr_data_std[-1]
            # Make a prediction using the model
            prediction = model(current_features_std.reshape(1, -1))
            predictions.append(prediction[0][0])
            predictions_array = np.array(predictions)

            # Plot Probability and shaded area
            axs[5].clear()
            axs[5].plot(t3, predictions_array, color='black')
            #axs[5].plot(t3, predictions_array, color='black')
            axs[5].set_title('Probability')
            axs[5].set_xlabel('Time (s)')
            axs[5].set_ylabel('Probability')
            axs[5].axhline(y=0.5, linestyle='--', color='red')
            axs[5].set_ylim([0, 1])
            axs[5].fill_between(t3, predictions_array, where=(predictions_array >= 0.5), color='red', alpha=0.3, linewidth=2.5)
            #axs[5].fill_between(t3, predictions_array, where=(predictions_array >= 0.5), color='red', alpha=0.3, linewidth=2.5, step='post')
            
    plt.tight_layout()
    frame_count += 1  # Increment frame count

# Set animation parameters
num_frames = 200
interval = 1000  # milliseconds

# Set up plot
fig, axs = plt.subplots(6, 1, figsize=(15, 10), sharex=True)

# Create animation object
ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=interval, blit=False)

# Show the animation
plt.show()

# Close the display and save the animation after 200 frames
# Save the animation as an MP4 movie
writer = FFMpegWriter(fps=1, metadata=dict(artist='Your Name'), bitrate=1800)
ani.save('ecg_signal_animation_with_noise2.mp4', writer=writer)
