#include "rocketData.h"

void createRocketPacket2017(RocketPacket& rp, int timestamp) {
  rp.rocketData.timeStamp = timestamp;
  rp.rocketData.angSpeedX = 0;
  rp.rocketData.angSpeedY = 0;
  rp.rocketData.angSpeedZ = 0;
  rp.rocketData.accelX = 0;
  rp.rocketData.accelY = accel(timestamp);
  rp.rocketData.accelZ = 0;
  rp.rocketData.altitude = altitude(timestamp);
  rp.rocketData.latitude = latitude(timestamp);
  rp.rocketData.longitude = longitude(timestamp);
  rp.rocketData.temperature = temperature1(timestamp);
  rp.rocketData.quaterniona = quaternionA(timestamp);
  rp.rocketData.quaternionb = quaternionB(timestamp);
  rp.rocketData.quaternionc = quaternionC(timestamp);
  rp.rocketData.quaterniond = quaternionD(timestamp);
  rp.rocketData.etatBoardAcquisition1 = etatBoard(timestamp);
  rp.rocketData.etatBoardAcquisition2 = etatBoard(timestamp);
  rp.rocketData.etatBoardAcquisition3 = etatBoard(timestamp);
  rp.rocketData.etatBoardAlim1 = etatBoard(timestamp);
  rp.rocketData.etatBoardAlim2 = 0;
  rp.rocketData.etatBoardPayload1 = etatBoard(timestamp);
  rp.rocketData.voltage = 3.3;
  rp.rocketData.courant = 0.001;
  rp.checksum = computeCheckSum(&(rp.rocketData), sizeof(RocketData));
}

