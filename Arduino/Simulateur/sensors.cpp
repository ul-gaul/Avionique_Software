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
  float t = (float)timestamp / FREQUENCY - T_TAKEOFF;
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

float latitude(int timestamp)
{
  float t = (float)timestamp / FREQUENCY - T_TAKEOFF;
  if(timestamp < T_TAKEOFF * FREQUENCY)
  {
    return 32.990524;
  }
  else if(timestamp < T_APOGEE * FREQUENCY)
  {
    return 0.00001836 * t + 32.990524;
  }
  else if (timestamp < T_PARACHUTE * FREQUENCY)
  {
    return -0.000007254 * t + 32.991164;
  }
  else if (timestamp < T_LANDING * FREQUENCY)
  {
    return -0.000071927 * t + 33.000671;
  }
  else
  {
    return 32.984128;
  }
}

float longitude(int timestamp)
{
  float t = (float)timestamp / FREQUENCY - T_TAKEOFF;
  if(timestamp < T_TAKEOFF * FREQUENCY)
  {
    return -106.975250;
  }
  else if(timestamp < T_APOGEE * FREQUENCY)
  {
    return 0.000021 * t - 106.975250;
  }
  else if (timestamp < T_PARACHUTE * FREQUENCY)
  {
    return 0.000008934 * t - 106.974948;
  }
  else if (timestamp < T_LANDING * FREQUENCY)
  {
    return -0.000082204 * t - 106.9615509;
  }
  else
  {
    return -106.980458;
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

