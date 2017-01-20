import serial
import csv
from datetime import datetime

from rocket_data.rocket_packet import RocketPacket
from communication.DetectSerial import serial_port


BAUDRATE = 57600
START_CHARACTER = b's'
PACKET_SIZE = 69


if __name__ == "__main__":
    # Connecting to serial port
    port_number = serial_port()[0]
    device = serial.Serial(port_number, baudrate=BAUDRATE, timeout=0.2)
    # device = serial.Serial("COM7", baudrate=BAUDRATE, timeout=0.2)

    # initializing csv file
    file_name = "output_files/{}_acquisition_data_basic.csv".format(datetime.now().strftime("%Y%m%d_%H%M%S"))
    print("File Name = {}".format(file_name))
    csv_file = open(file_name, 'a', newline='')
    writer = csv.writer(csv_file)
    writer.writerow(["TIME STAMP", "ANG SPEED X", "ANG SPEED Y", "ANG SPEED Z", "ACCEL X", "ACCEL Y", "ACCEL Z", "MAGNET X", "MAGNET Y", "MAGNET Z", "ALTITUDE", "LATITUDE 1", "LONGITUDE 1", "LATITUDE 2", "LONGITUDE 2", "TEMPERATURE 1", "TEMPERATURE 2"])

    while True:
        c = device.read(1)
        if c != b'':
            print(c)
        if c == START_CHARACTER:
            print("Received first character")
            while device.inWaiting() < PACKET_SIZE:
                pass
            data = device.read(PACKET_SIZE)

            rocket_data = RocketPacket(data)
            # checksum_validated = rocket_data.validateCheckSum()
            checksum_validated = True
            print("Checksum validated : {}".format(checksum_validated))
            if checksum_validated: # TODO Validate checksum for real!!!
                rocket_data.print_data()
                writer.writerow([rocket_data.time_stamp, rocket_data.angular_speed_x, rocket_data.angular_speed_y, rocket_data.angular_speed_z, rocket_data.acceleration_x, rocket_data.acceleration_y, rocket_data.acceleration_z, rocket_data.magnetic_field_x, rocket_data.magnetic_field_y, rocket_data.magnetic_field_z, rocket_data.altitude, rocket_data.latitude_1, rocket_data.longitude_1, rocket_data.latitude_2, rocket_data.longitude_2, rocket_data.temperature_1, rocket_data.temperature_2] + [None])
                csv_file.flush()