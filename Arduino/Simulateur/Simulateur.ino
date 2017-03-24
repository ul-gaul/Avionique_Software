#include "rocketData.h"
#include "sensors.h"

#define START_BYTE 's'

int timestamp = 0;

byte computeCheckSum(byte *data)
{
  byte sum = 0;
  for(int i = 0; i < sizeof(RocketData); i++)
  {
    sum += data[i];
  }
  return ~sum;
}

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop()
{
  RocketPacket rp;
  rp.rocketData.timeStamp = timestamp;
  rp.rocketData.angSpeedX = 0;
  rp.rocketData.angSpeedY = 0;
  rp.rocketData.angSpeedZ = 0;
  rp.rocketData.accelX = 0;
  rp.rocketData.accelY = accel(timestamp);
  rp.rocketData.accelZ = 0;
  rp.rocketData.magnetX = 0;
  rp.rocketData.magnetY = 0;
  rp.rocketData.magnetZ = 0;
  rp.rocketData.altitude = altitude(timestamp);
  rp.rocketData.latitude1 = latitude(timestamp);
  rp.rocketData.longitude1 = longitude(timestamp);
  rp.rocketData.latitude2 = latitude(timestamp);
  rp.rocketData.longitude2 = longitude(timestamp);
  rp.rocketData.temperature1 = temperature1(timestamp);
  rp.rocketData.temperature2 = temperature2(timestamp);
  rp.rocketData.temperature3 = temperature1(timestamp);
  rp.rocketData.timeStampDate = 0;
  rp.rocketData.quaterniona = 0;
  rp.rocketData.quaternionb = 0;
  rp.rocketData.quaternionc = 0;
  rp.rocketData.quaterniond = 0;
  rp.rocketData.etatBoardAcquisition1 = 255;
  rp.rocketData.etatBoardAcquisition2 = 255;
  rp.rocketData.etatBoardAcquisition3 = 255;
  rp.rocketData.etatBoardAlim1 = 255;
  rp.rocketData.etatBoardAlim2 = 255;
  rp.rocketData.etatBoardPayload1 = etatBoard(timestamp);
  rp.rocketData.voltage = 3.3;
  rp.rocketData.courant = 0.001;
  rp.rocketData.angSpeedXPayload = 0;
  rp.rocketData.angSpeedYPayload = 0;
  rp.rocketData.angSpeedZPayload = 0;
  rp.rocketData.camera = 128;
  rp.rocketData.deploiement = 255;

  //Calcul du checksum
  byte dataBuffer[sizeof(RocketData)];
  memcpy(dataBuffer, &(rp.rocketData), sizeof(RocketData));
  rp.checksum = computeCheckSum(dataBuffer);

  //Envoi du packet sur le port serie
  byte packetBuffer[sizeof(RocketPacket)];
  memcpy(packetBuffer, &rp, sizeof(RocketPacket));
  Serial.write(START_BYTE);
  Serial.write(packetBuffer, sizeof(RocketPacket));

  timestamp++;
  delay(200);
}
