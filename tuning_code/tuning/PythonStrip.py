import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# Set up serial connection
ser = serial.Serial('COM_PORT', 9600)  # Replace 'COM_PORT' with your actual COM port, e.g., 'COM4' or '/dev/ttyUSB0'

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
            u_val = int(data[0].split(':')[1])
            d_val = int(data[1].split(':')[1])
            l_val = int(data[2].split(':')[1])
            r_val = int(data[3].split(':')[1])
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

    ax.clear()
    ax.plot(data_U, label='U')
    ax.plot(data_D, label='D')
    ax.plot(data_L, label='L')
    ax.plot(data_R, label='R')
    ax.set_ylim([0, 1023])
    ax.legend(loc='upper right')

# Set up plot
fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, fargs=(data_U, data_D, data_L, data_R), interval=50)

# Display plot
plt.show()