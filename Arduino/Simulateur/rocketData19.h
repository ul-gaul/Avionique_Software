#ifndef _rocketData19_h
#define _rocketData19_h

#include "Arduino.h"
#include "sensors.h"
#include "convertor.h"

#define GPS_FIX_DELAY 3

typedef struct {
  // time since boot in milliseconds
  byte timestamp[8]; // 8
  // GPS values
  byte latitude[8]; // 16
  byte longitude[8]; // 24
  char NSIndicator; // 32
  char EWIndicator; // 40
  byte UTCTime[8]; // 48
  // 10DOF values
  // BMP180

  float altitude; // 52
  uint32_t pressure; // 56
  float temperature; // 60
  // lsm303
  // acceleration values are in milli-G
  int16_t acc_x_uncomp; // 62
  int16_t acc_y_uncomp; // 64
  int16_t acc_z_uncomp; // 66
  float acc_x; // 70
  float acc_y; // 74
  float acc_z; // 78
  // magnetic field values are in milli-gauss
  int16_t mag_x; // 80
  int16_t mag_y; // 82
  int16_t mag_z; // 84
  // l3dg20
  // angular speed values are in degrees/s
  int16_t x_gyro; // 86
  int16_t y_gyro; // 88
  int16_t z_gyro; // 90
} RocketData19;

typedef struct {
  RocketData19 data;
  byte checksum;
} RocketPacket19;

void createRocketPacket2019(RocketPacket19& rp, int timestamp);

#endif
