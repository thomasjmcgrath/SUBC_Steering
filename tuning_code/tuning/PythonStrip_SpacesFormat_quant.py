import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

def quantize_data(u_val, d_val, l_val, r_val, num_levels=10):
    max_value = 1023
    step = max_value // (num_levels - 1)

    u_val_quantized = (u_val // step) * step
    d_val_quantized = (d_val // step) * step
    l_val_quantized = (l_val // step) * step
    r_val_quantized = (r_val // step) * step

    return u_val_quantized, d_val_quantized, l_val_quantized, r_val_quantized

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
        u_val, d_val, l_val, r_val = quantize_data(u_val, d_val, l_val, r_val)  # Add this line to quantize the data
        data_U.append(u_val)
        data_D.append(d_val)
        data_L.append(l_val)
        data_R.append(r_val)

    ax.clear()
    ax.plot(data_U, label='Up')
    ax.plot(data_D, label='Down')
    ax.plot(data_L, label='Left')
    ax.plot(data_R, label='Right')
    ax.set_ylim([0, 1023])
    ax.legend(loc='upper right')


# Set up plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, fargs=(data_U, data_D, data_L, data_R), interval=50)

# Display plot
plt.show()