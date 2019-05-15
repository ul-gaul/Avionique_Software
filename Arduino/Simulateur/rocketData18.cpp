#include "rocketData18.h"

void createRocketPacket2018(RocketPacket18& rp, int timestamp) {
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
}

