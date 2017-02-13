#include "sensors.h"

float accel(int timestamp)
{
  if(timestamp < 150)
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
  if(timestamp < 150)
  {
    return -(4.0/9.0)*(timestamp-150)*(timestamp-150) + 10000;
  }
  else if (timestamp >= 150 && timestamp < 3275)
  {
    return 10000-16.0*timestamp/5;
  }
  else
  {
    return 0.0;
  }
}

float latitude(int timestamp)
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

float longitude(int timestamp)
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
  if(timestamp < 30)
  {
    return 0;
  }
  else if(timestamp >= 30 && timestamp < 150)
  {
    return 255;
  }
  else
  {
    return 128;
  }
}

