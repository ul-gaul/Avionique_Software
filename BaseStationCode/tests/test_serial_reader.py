from src.serial_reader import SerialReader
from time import sleep

if __name__ == "__main__":
    reader = SerialReader()
    reader.start()
    for i in range(200):
        packets = reader.get_data()
        if len(packets) > 0:
            packets[-1].print_data()
        sleep(0.2)
    reader.stop()
