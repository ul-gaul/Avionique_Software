#include "sensors.h"

float accel(int timestamp)  //TODO
{
  if(timestamp < T_TAKEOFF * FREQUENCY)
  {
    return -9.8;
  }
  else if(timestamp < T_PARACHUTE * FREQUENCY)
  {
    return (-4.0/9.0);
  }
  else
  {
    return 0.0;
  }
}

float altitude(int timestamp)
{
  float t = (timestamp - T_TAKEOFF) * FREQUENCY;
  if(timestamp < T_TAKEOFF * FREQUENCY)
  {
    return 0;
  }
  else if(timestamp < T_ENGINE * FREQUENCY)
  {
    return 30.123 * t * t;
  }
  else if (timestamp < T_APOGEE * FREQUENCY)
  {
    return -0.626 * t * t + 138.373 * t;
  }
  else if (timestamp < T_PARACHUTE * FREQUENCY)
  {
    return -20.15 * t + 3571.75;
  }
  else if (timestamp < T_LANDING * FREQUENCY)
  {
    return -7.35 * t + 1690.45;
  }
  else
  {
    return 0;
  }
}

float latitude(int timestamp) //TODO
{
  if(timestamp < 150)
  {
    return 0.0;
  }
  else if(timestamp >= 150 && timestamp < 3275)
  {
    return 1.0*(timestamp-150);
  }
  else
  {
    return 3125.0;
  }
}

float longitude(int timestamp)  //TODO
{
  if(timestamp < 150)
  {
    return 0.0;
  }
  else if(timestamp >= 150 && timestamp < 3275)
  {
    return -0.5*(timestamp-150);
  }
  else
  {
    return -1562.5;
  }
}

float temperature1(int timestamp)
{
  return 3*cos(timestamp*M_PI/25) + 100;
}

float temperature2(int timestamp)
{
  return 2*sin(timestamp*M_PI/25) + 102;
}

uint8_t etatBoard(int timestamp)
{
  if(timestamp < T_BOARD_ON * FREQUENCY)
  {
    return 0;
  }
  else
  {
    return 255;
  }
}

