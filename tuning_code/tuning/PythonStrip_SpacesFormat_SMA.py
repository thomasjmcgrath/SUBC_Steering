import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

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

    ax.clear()
    ax.plot(filtered_data_U, label='Up')
    ax.plot(filtered_data_D, label='Down')
    ax.plot(filtered_data_L, label='Left')
    ax.plot(filtered_data_R, label='Right')
    ax.set_ylim([0, 1023])
    ax.legend(loc='upper right')


# Set up plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, fargs=(data_U, data_D, data_L, data_R), interval=50)

# Display plot
plt.show()