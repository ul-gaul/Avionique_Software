# pylint: skip-file
import time

from src.file_reader import FileReader

myFileReader = FileReader("resources/TestFile.csv")

allPacket = myFileReader.get_data()

print(str(len(allPacket)))

myFileReader.start()

for i in range(0,50,1):

    time.sleep(0.25)
    if (not myFileReader.rocket_packets.empty()):
        packetList = myFileReader.get_data()
        for packet in packetList:
            print(packet.print_data())
            print("----------------------------------------------------------------------------------------\n")


myFileReader.stop()
