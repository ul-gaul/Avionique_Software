#ifndef _rocketData18_h
#define _rocketData18_h

#include "Arduino.h"

typedef struct
{
  unsigned long timestamp;
  // GPS values
  float latitude;
  float longitude;
  // 10DOF values
  float altitude;
  float temperature;
  float x_accel;
  float y_accel;
  float z_accel;
  float x_magnet;
  float y_magnet;
  float z_magnet;
  float x_gyro;
  float y_gyro;
  float z_gyro;
} RocketData18;

typedef struct
{
  RocketData18 rocketData;
  byte checksum;
} RocketPacket18;

#endif
