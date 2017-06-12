#ifndef _rocketData_h
#define _rocketData_h

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
    float temperature3; //on a seulement 2 capteurs dans la fusée, le 3e va être la moyenne des deux...
    //add more temperature entries here if needed

    //nouveau depuis 2016/2017:
    float timeStampDate; //date du module RTC

    //position avec le bno055
    float quaterniona;
    float quaternionb;
    float quaternionc;
    float quaterniond;

    //états des systèmes (on pourrait prendre des bools mais j'aime mieux mettre des int pour mettre plus d'informations en fesant de la manipulation de bit)
    uint8_t etatBoardAcquisition1; //c'est le board que j'appelle GPS1, il contient le premier GPS et un MPU6050 (ang + accel)
    uint8_t etatBoardAcquisition2; //c'est le board que j'appelle 9DOF, il contient un capteur de température et un BN055 (quaternions)
    uint8_t etatBoardAcquisition3; //c'est le board que j'appelle GPS2, il contient le 2e GPS et un capteur de température
    uint8_t etatBoardAlim1; //état de l'alimentation principale
    uint8_t etatBoardAlim2; //pas utilisé pour l'instant
    uint8_t etatBoardPayload1; //c'est le board qui contrôle la fibre optique

    //données alim
    float voltage; //pas utilisé pour l'instant
    float courant; //pas utilisé pour l'instant

    //données payload
    float angSpeedXPayload;
    float angSpeedYPayload;
    float angSpeedZPayload;

    //données contrôle (qui ne seront probablement pas utilisées mais on sait jamais)
    uint8_t camera; //pas utilisé pour l'instant
    uint8_t deploiement; //pas utilisé pour l'instant 



} RocketData;

typedef struct
{
  RocketData rocketData;
	byte checksum;
} RocketPacket;

#endif
