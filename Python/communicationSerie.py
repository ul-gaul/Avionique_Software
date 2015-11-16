from time import sleep
import serial

ser = serial.Serial('COM3', 9600,timeout = 0) # Establish the connection on a specific port
#ser.open()
#ser.isopen()
#ser.write(b'5')
while True:
    #value = ser.readline().decode().strip()
    value = ser.readline()
    #value = ser.read(2)
    ser.flushInput()
    try:
        #if value:
           # print(ord(value))
        #print(float(value))
        print(ord(value))
        #print(value)
        sleep(0.05)
    
    except ValueError:
        #print(value + "E")
        print("erreur")
        sleep(0.05)
    except:
        print("erreur" + str(value.decode()) + "end")
    #except ser.SerialTimeoutException:
        #print('Data could not be read')
        #sleep(1)
    
    
