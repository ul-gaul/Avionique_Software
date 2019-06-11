#include "rocketData19.h"

void createRocketPacket2019(RocketPacket19& rp, int timestamp) {
  toDouble((float)timestamp, rp.data.timestamp);
  toDouble(dd2ddmm(latitude(timestamp)), rp.data.latitude);
  toDouble(dd2ddmm(longitude(timestamp)), rp.data.longitude);
  rp.data.NSIndicator = 'N';
  rp.data.EWIndicator = 'W';
  toDouble(123.36, rp.data.UTCTime);
  rp.data.altitude = altitude(timestamp);
  rp.data.pressure = pressure(timestamp);
  rp.data.temperature = temperature1(timestamp);
  rp.data.acc_x_uncomp = 0;
  rp.data.acc_y_uncomp = 0;
  rp.data.acc_z_uncomp = 0;
  rp.data.acc_x = 0;
  rp.data.acc_y = 0;
  rp.data.acc_z = accel(timestamp);
  rp.data.mag_x = (int16_t) magnetX(timestamp);
  rp.data.mag_y = 4321;
  rp.data.mag_z = (int16_t) magnetZ(timestamp);
  rp.data.x_gyro = 0;
  rp.data.y_gyro = 0;
  rp.data.z_gyro = 42;

  rp.checksum = computeCheckSum(&(rp.data), sizeof(RocketData19));
}

