import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from pykalman import KalmanFilter
import numpy as np

class KalmanFilter1D:
    def __init__(self, initial_estimate, process_variance, measurement_variance):
        self.estimate = initial_estimate
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance
        self.error_variance = 1

    def update(self, measurement):
        kalman_gain = self.error_variance / (self.error_variance + self.measurement_variance)
        self.estimate = self.estimate + kalman_gain * (measurement - self.estimate)
        self.error_variance = (1 - kalman_gain) * self.error_variance + self.process_variance


# Set up serial connection
ser = serial.Serial("COM4", 9600) 
# Set up deque to store data
window_size = 100
data_U = deque([0] * window_size, maxlen=window_size)
data_D = deque([0] * window_size, maxlen=window_size)
data_L = deque([0] * window_size, maxlen=window_size)
data_R = deque([0] * window_size, maxlen=window_size)

initial_estimate = 0
process_variance = 1
measurement_variance = 10

kf_U = KalmanFilter1D(initial_estimate, process_variance, measurement_variance)
kf_D = KalmanFilter1D(initial_estimate, process_variance, measurement_variance)
kf_L = KalmanFilter1D(initial_estimate, process_variance, measurement_variance)
kf_R = KalmanFilter1D(initial_estimate, process_variance, measurement_variance)


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
        # Update Kalman filters
        kf_U.update(u_val)
        kf_D.update(d_val)
        kf_L.update(l_val)
        kf_R.update(r_val)

        # Append filtered data to deques
        data_U.append(kf_U.estimate)
        data_D.append(kf_D.estimate)
        data_L.append(kf_L.estimate)
        data_R.append(kf_R.estimate)

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