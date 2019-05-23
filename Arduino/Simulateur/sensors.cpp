#include "sensors.h"

float accel(int timestamp)  //TODO
{
  if (timestamp < T_TAKEOFF * FREQUENCY)
  {
    return -9.8;
  }
  else if (timestamp < T_PARACHUTE * FREQUENCY)
  {
    return (-4.0 / 9.0);
  }
  else
  {
    return 0.0;
  }
}

float altitude(int timestamp)
{
  float t = (float)timestamp / FREQUENCY - T_TAKEOFF;
  if (timestamp < T_TAKEOFF * FREQUENCY)
  {
    return 0;
  }
  else if (timestamp < T_ENGINE * FREQUENCY)
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
  if (timestamp < T_TAKEOFF * FREQUENCY)
  {
    return 32.990524;
  }
  else if (timestamp < T_APOGEE * FREQUENCY)
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
  if (timestamp < T_TAKEOFF * FREQUENCY)
  {
    return -106.975250;
  }
  else if (timestamp < T_APOGEE * FREQUENCY)
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

uint32_t pressure(int timestamp) {
  return 1013;
}

float temperature1(int timestamp)
{
  return 5 * cos(timestamp * M_PI / 25) + 45;
}

float temperature2(int timestamp)
{
  return 2 * sin(timestamp * M_PI / 25) + 102;
}

float quaternionA(int timestamp)
{
  return (5 * timestamp) % 360;
}

float quaternionB(int timestamp)
{
  return 0.5;
}

float quaternionC(int timestamp)
{
  return 0;
}

float quaternionD(int timestamp)
{
  return 0.5;
}

uint8_t etatBoard(int timestamp)
{
  if (timestamp < T_BOARD_ON * FREQUENCY)
  {
    return 0;
  }
  else
  {
    return 255;
  }
}

float payloadX(int timestamp)
{
  return 5.0;
}

float payloadY(int timestamp)
{
  return 1023.0;
}

float payloadZ(int timestamp)
{
  return 600.0;
}

float magnetX(int timestamp)
{
  float t = (float)timestamp / FREQUENCY - T_TAKEOFF;
  if (timestamp < T_ENGINE * FREQUENCY)
  {
    return 90;
  }
  else if (timestamp < T_APOGEE * FREQUENCY)
  {
    return 87;
  }
  else if (timestamp < T_PARACHUTE * FREQUENCY)
  {
    return -90;
  }
  else if (timestamp < T_LANDING * FREQUENCY)
  {
    return 90;
  }
  else
  {
    return 0;
  }
}

float magnetZ(int timestamp)
{
  float t = (float)timestamp / FREQUENCY - T_TAKEOFF;
  if (timestamp < T_TAKEOFF * FREQUENCY)
  {
    return 0;
  }
  else if (timestamp < T_ENGINE * FREQUENCY)
  {
    return sin(timestamp * M_PI / 10);
  }
  else if (timestamp < T_APOGEE * FREQUENCY)
  {
    return 2 * sin(timestamp * M_PI / 10);
  }
  else if (timestamp < T_PARACHUTE * FREQUENCY)
  {
    return 5 * sin(timestamp * M_PI / 10);
  }
  else
  {
    return 0;
  }
}

byte computeCheckSum(void* data, size_t numBytes)
{
  byte sum = 0;
  for (int i = 0; i < numBytes; i++)
  {
    sum += ((byte*)data)[i];
  }
  return ~sum;
}

