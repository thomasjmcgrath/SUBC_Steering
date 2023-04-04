import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np


# Initialize SMA filter
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

# Initialize the Kalman filter
def kalman_filter(data, process_noise, measurement_noise, initial_estimate=530):
    x = initial_estimate
    error_estimate = 100
    filtered_data = []

    for z in data:
        # Time update (prediction step)
        x_prior = x
        error_estimate_prior = error_estimate + process_noise

        # Measurement update (correction step)
        kalman_gain = error_estimate_prior / (error_estimate_prior + measurement_noise)
        x = x_prior + kalman_gain * (z - x_prior)
        error_estimate = (1 - kalman_gain) * error_estimate_prior

        filtered_data.append(x)

    return np.array(filtered_data)


# Set up serial connection
ser = serial.Serial("COM4", 9600) 
# Set up deque to store data
window_size = 100
data_U = deque([0] * window_size, maxlen=window_size)
data_D = deque([0] * window_size, maxlen=window_size)
data_L = deque([0] * window_size, maxlen=window_size)
data_R = deque([0] * window_size, maxlen=window_size)

def read_serial_data():
    ser_line = ser.readline().decode('utf-8').strip()
    data = ser_line.split(' ')
    
    if len(data) == 4:
        try:
            u_val = int(data[0])
            d_val = int(data[1])
            l_val = int(data[2])
            r_val = int(data[3])
            return u_val, d_val, l_val, r_val
        except ValueError:
            pass
    
    return None, None, None, None

def update(frame, data_U, data_D, data_L, data_R):
    u_val, d_val, l_val, r_val = read_serial_data()

    if u_val is not None:
        data_U.append(u_val)
        data_D.append(d_val)
        data_L.append(l_val)
        data_R.append(r_val)

    # Apply moving average filter
    sma_window_size = 5  # Adjust the window size as needed
    filtered_data_U = moving_average(data_U, sma_window_size)
    filtered_data_D = moving_average(data_D, sma_window_size)
    filtered_data_L = moving_average(data_L, sma_window_size)
    filtered_data_R = moving_average(data_R, sma_window_size)

    # Apply Kalman filter
    process_noise = 0.001
    measurement_noise = 200
    kf_data_U = kalman_filter(filtered_data_U, process_noise, measurement_noise)
    kf_data_D = kalman_filter(filtered_data_D, process_noise, measurement_noise)
    kf_data_L = kalman_filter(filtered_data_L, process_noise, measurement_noise)
    kf_data_R = kalman_filter(filtered_data_R, process_noise, measurement_noise)

    ax.clear()
    ax.plot(kf_data_U, label='Up')
    ax.plot(kf_data_D, label='Down')
    ax.plot(kf_data_L, label='Left')
    ax.plot(kf_data_R, label='Right')
    ax.set_ylim([0, 1023])
    ax.legend(loc='upper right')




# Set up plot

fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, fargs=(data_U, data_D, data_L, data_R), interval=50)

# Display plot
plt.show()