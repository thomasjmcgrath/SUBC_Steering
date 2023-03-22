import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ser = serial.Serial("COM3", 9600)  # Change "COM3" to the appropriate port for your Arduino

def read_serial_data():
    ser.flushInput()
    raw_data = ser.readline().decode('utf-8').strip()
    values = [int(x) for x in raw_data.split(' ') if x.isdigit()]
    if len(values) == 4:
        return values
    else:
        return [0, 0, 0, 0]

fig, ax = plt.subplots()
x = [0, 1, 2, 3]
bar_width = 0.4
bars = plt.bar(x, [0, 0, 0, 0], bar_width)

def update_bars(frame):
    values = read_serial_data()
    for i, bar in enumerate(bars):
        bar.set_height(values[i])

ani = FuncAnimation(fig, update_bars, interval=100, blit=False)
plt.xticks(x, ['Value 1', 'Value 2', 'Value 3', 'Value 4'])
plt.ylim([0, 1023])
plt.show()

ser.close()