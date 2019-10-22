#include "rocketData19.h"

float simulateLatitude(int timestamp) {
    if (timestamp >= GPS_FIX_DELAY) {
        return dd2ddmm(latitude(timestamp));
    } else {
        return NO_FIX;
    }
}

float simulateLongitude(int timestamp) {
    if (timestamp >= GPS_FIX_DELAY) {
        return dd2ddmm(longitude(timestamp));
    } else {
        return NO_FIX;
    }
}

void createRocketPacket2019(RocketPacket19& rp, int timestamp) {
  toDouble((float)timestamp, rp.data.timestamp);

  toDouble(simulateLatitude(timestamp), rp.data.latitude);
  toDouble(simulateLongitude(timestamp), rp.data.longitude);
  rp.data.NSIndicator = timestamp >= GPS_FIX_DELAY ? 'N' : 'M';
  rp.data.EWIndicator = timestamp >= GPS_FIX_DELAY ? 'W' : 'F';

  toDouble(123.36, rp.data.UTCTime);
  rp.data.altitude = altitude(timestamp);
  rp.data.pressure = pressure(timestamp);
  rp.data.temperature = temperature1(timestamp);

  rp.data.acc_x_uncomp = 0;
  rp.data.acc_y_uncomp = 0;
  rp.data.acc_z_uncomp = 0;

  rp.data.acc_x = 0;
  rp.data.acc_y = 707;
  rp.data.acc_z = 707;

  rp.data.mag_x = (int16_t) magnetX(timestamp);
  rp.data.mag_y = 4321;
  rp.data.mag_z = (int16_t) magnetZ(timestamp);

  rp.data.x_gyro = 2;
  rp.data.y_gyro = 0;
  rp.data.z_gyro = 0;

  rp.checksum = computeCheckSum(&(rp.data), sizeof(RocketData19));
}

