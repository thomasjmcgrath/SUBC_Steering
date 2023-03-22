"""
============
Strip Chart
============


based on example
https://matplotlib.org/stable/gallery/animation/strip_chart.html#sphx-glr-gallery-animation-strip-chart-py

"""
import serial
import serial.tools.list_ports
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

class Scope:
    def __init__(self, ax, maxt=25, dt=0.075): #maxt is the t-axis length and dt is the change per tick
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        self.ax.set_ylim(-1000, 2023)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt: 
            self.ax.set_xlim(self.tdata[-1]-self.maxt, self.tdata[-1])

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,

def serial_values():
    #read existing on serial and get last line
    strin = ser.readline()
    try:
        val = strin.decode('utf-8')
              #for debugging purposes 
        voltage = float(val.replace("\r\n",""))
        print(val)                             #check flag to see if we are measuring voltage or temperature 
        plt.ylabel("Voltage (V)")
        yield voltage

    except:
        pass

# configure the serial port
try:
    ser = serial.Serial(
        port='COM4', # Change as needed
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS
    )
    ser.isOpen()
except:
    portlist=list(serial.tools.list_ports.comports())
    print ('Available serial ports:')
    for item in portlist:
       print (item[0])
    print ('Please change serial ports')
    exit()

fig, ax = plt.subplots()
scope = Scope(ax)

# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, scope.update, serial_values, interval=25,
                              blit=False, repeat=True)

plt.xlabel("Time (s)")
plt.minorticks_on()
plt.grid(which='major', color = 'blue', linestyle = '--', linewidth = 0.5)
plt.grid(which='minor', color = 'black', linestyle = '--', linewidth = 0.25)
plt.show()