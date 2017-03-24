#ifndef _sensors_h
#define _sensors_h

#include "Arduino.h"
#include "math.h"

float accel(int timestamp);
float altitude(int timestamp);
float latitude(int timestamp);
float longitude(int timestamp);
float temperature1(int timestamp);
float temperature2(int timestamp);
uint8_t etatBoard(int timestamp);

#endif
