import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
import numpy as np
import scipy.signal

def savitzky_golay_filter(data, window_size, polynomial_order):
    return scipy.signal.savgol_filter(data, window_size, polynomial_order)

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

    # Apply Savitzky-Golay filter
    sg_window_size = 5  # Adjust the window size as needed; must be an odd integer
    sg_polynomial_order = 3  # Adjust the polynomial order as needed
    filtered_data_U = savitzky_golay_filter(data_U, sg_window_size, sg_polynomial_order)
    filtered_data_D = savitzky_golay_filter(data_D, sg_window_size, sg_polynomial_order)
    filtered_data_L = savitzky_golay_filter(data_L, sg_window_size, sg_polynomial_order)
    filtered_data_R = savitzky_golay_filter(data_R, sg_window_size, sg_polynomial_order)

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