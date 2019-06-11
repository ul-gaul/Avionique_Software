#ifndef _sensors_h
#define _sensors_h

#include "Arduino.h"
#include "math.h"

#define FREQUENCY     1.0     //Sampling frequency (Hz)
#define H_APOGEE      3067  //Apogee (m)
#define H_ENGINE      610   //End of combustion altitude (m)
#define H_PARACHUTE   610   //Main parachute deploiment altitude (m)
#define T_BOARD_ON    5     //Delay before the boards are turned on (sec)
#define T_TAKEOFF     10    //Delay before takeoff (sec)
#define T_ENGINE      14.5  //Delay before end of combustion (sec)
#define T_APOGEE      35    //Delay before apogee (sec)
#define T_PARACHUTE   157   //Delay before main parachute deploiment (sec)
#define T_LANDING     240   //Delay before landing (sec)

float accel(int timestamp);
float altitude(int timestamp);
float latitude(int timestamp);
float longitude(int timestamp);
float dd2ddmm(float dd_coordinate);
uint32_t pressure(int timestamp);
float temperature1(int timestamp);
float temperature2(int timestamp);
float quaternionA(int timestamp);
float quaternionB(int timestamp);
float quaternionC(int timestamp);
float quaternionD(int timestamp);
uint8_t etatBoard(int timestamp);
float payloadX(int timestamp);
float payloadY(int timestamp);
float payloadZ(int timestamp);
float magnetX(int timestamp);
float magnetZ(int timestamp);

byte computeCheckSum(void* data, size_t numBytes);

#endif
