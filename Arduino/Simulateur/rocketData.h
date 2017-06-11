#ifndef _rocketData_h
#define _rocketData_h

#include "Arduino.h"

typedef struct
{
    //Time Stamp
    float timeStamp;

    //Angular Speed in Radian per Second
  	float angSpeedX;
  	float angSpeedY;
  	float angSpeedZ;
  
  	//Acceleration in g
  	float accelX;
  	float accelY;
  	float accelZ;
  
  	//Altitude in meter (avec un bmp180)
  	float altitude;
  
  	//GPS Coordinates in degrees (2e set est possible qu'il ne soit pas là)
  	float latitude1;
  	float longitude1;
  	float latitude2; 
  	float longitude2;

    //Temperature in Celsius degrees
    float temperature1;
    float temperature2;
    float temperature3;
    //add more temperature entries here if needed


    //nouveau depuis 2016/2017:

    float timeStampDate;

    //position avec le bno055
    float quaterniona;
    float quaternionb;
    float quaternionc;
    float quaterniond;

    //états des systèmes (on pourrait prendre des bools mais j'aime mieux mettre des int pour mettre plus d'informations en fesant de la manipulation de bit)
    uint8_t etatBoardAcquisition1;
    uint8_t etatBoardAcquisition2;
    uint8_t etatBoardAcquisition3;
    uint8_t etatBoardAlim1;
    uint8_t etatBoardAlim2;
    uint8_t etatBoardPayload1;

    //données alim
    float voltage;
    float courant;

    //données payload
    float angSpeedXPayload;
    float angSpeedYPayload;
    float angSpeedZPayload;

    //données contrôle (qui ne seront probablement pas utilisées mais on sait jamais)
    uint8_t camera;
    uint8_t deploiement;
} RocketData;

typedef struct
{
  RocketData rocketData;
	byte checksum;
} RocketPacket;

#endif
