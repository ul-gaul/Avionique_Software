import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from time import sleep
import serial

#Section DetectSerial.py
#--------------------------------------------------------------
import sys
import glob
import serial



def serial_port():
    """ Lists serial port names

    :raises EnvironmentError
        On unsopported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i+1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
"""
if __name__ == '__main__':
    print(serial_port())
"""
portserie = serial_port()[0]
#--------------------------------------------------------------
#fin de la section DetectSerial.py


DELAY = 50 #delai, en millisecondes, entre les appels de la fonction animate

#values = [(1,2), (2,3), (3,6), (4,9), (5,4), (6,7), (7,7), (8,4), (9,3), (10,7)]
xar = []
yar1 = []
yar2 = []

ser = serial.Serial(portserie, 9600,timeout = 0)
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    value = ser.readline().decode().strip()
    ser.flushInput()
    try:
        #voltage = 5*int(value)/1023
        if(float(value) <= 5.0):
        #if(voltage <= 5.0):
            print(float(value))
            #print(voltage)
            xar.append(i*DELAY/1000)
            yar1.append(float(value))
            yar2.append(2.5*np.cos((i*DELAY/1000)*np.pi/20) + 2.5)
            #yar.append(voltage)

    
    except ValueError:
        print(value + "E")
    #pullData = open("sampleText.txt","r").read()
    #dataArray = pullData.split('\n')
    """
    for eachLine in dataArray:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xar.append(int(x))
            yar.append(int(y))
    """
    """
    for tuple in values[0:i+1]:
        if len(tuple) > 1:
            x,y = tuple
            xar.append(x)
            yar.append(y)
    """
    ax1.clear()
    ax1.plot(xar, yar2, "r--", xar, yar1)

ani = animation.FuncAnimation(fig, animate, interval=DELAY)
plt.show()
