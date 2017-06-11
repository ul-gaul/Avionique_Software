from src.serial_reader import SerialReader
from time import sleep

if __name__ == "__main__":
    freq = 1
    reader = SerialReader(frequency=freq)
    reader.start()
    for i in range(int(30*(1.0/freq))):
        packets = reader.get_data()
        for packet in packets:
            print(packet)
        sleep(freq)
    reader.stop()
