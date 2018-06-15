#include "rocketData.h"
#include "rocketData18.h"
#include "sensors.h"

#define START_BYTE 's'
#define ROCKET_PACKET_VERSION 2018
#define BAUDRATE 9600

int timestamp = 0;

byte computeCheckSum(void* data, size_t numBytes)
{
  byte sum = 0;
  for(int i = 0; i < numBytes; i++)
  {
    sum += ((byte*)data)[i];
  }
  return ~sum;
}

void writeToSerial(void* data, size_t numBytes)
{
  Serial.write(START_BYTE);
  Serial.write((byte*)data, numBytes);
}

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(BAUDRATE);
}

void loop()
{
  if (ROCKET_PACKET_VERSION == 2017)
  {
    RocketPacket rp;
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

    writeToSerial(&rp, sizeof(RocketPacket));
  }
  else if (ROCKET_PACKET_VERSION == 2018)
  {
    RocketPacket18 rp;
    rp.rocketData.timestamp = timestamp;
    rp.rocketData.latitude = latitude(timestamp);
    rp.rocketData.longitude = longitude(timestamp);
    rp.rocketData.altitude = altitude(timestamp);
    rp.rocketData.temperature = temperature1(timestamp);
    rp.rocketData.x_accel = 0;
    rp.rocketData.y_accel = 0;
    rp.rocketData.z_accel = accel(timestamp);
    rp.rocketData.x_magnet = magnetX(timestamp);
    rp.rocketData.y_magnet = 0;
    rp.rocketData.z_magnet = magnetZ(timestamp);
    rp.rocketData.x_gyro = 0;
    rp.rocketData.y_gyro = 0;
    rp.rocketData.z_gyro = 2;
    rp.checksum = computeCheckSum(&(rp.rocketData), sizeof(RocketData18));

    writeToSerial(&rp, sizeof(RocketPacket18));
  }
  
  timestamp++;
  delay(1000 * (1.0 / FREQUENCY));
}
