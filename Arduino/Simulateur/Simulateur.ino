#include "math.h"
#define numData 17

int timestamp = 0;

struct rocketPacket
{
  float array[numData];
};

byte computeCheckSum(byte array[numData*sizeof(float)])
{
  byte sum = 0;
  for(int i = 0; i < numData*sizeof(float); i++)
  {
    sum += array[i];
  }
  return sum;
}

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

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop()
{
  rocketPacket rp;
  rp.array[0] = timestamp;
  rp.array[1] = 0;
  rp.array[2] = 0;
  rp.array[3] = 0;
  rp.array[4] = accel(timestamp);
  rp.array[5] = 0;
  rp.array[6] = 0;
  rp.array[7] = 0;
  rp.array[8] = 0;
  rp.array[9] = 0;
  rp.array[10] = altitude(timestamp);
  rp.array[11] = latitude(timestamp);
  rp.array[12] = longitude(timestamp);
  rp.array[13] = latitude(timestamp);
  rp.array[14] = longitude(timestamp);
  rp.array[15] = temperature1(timestamp);
  rp.array[16] = temperature2(timestamp);
  
  byte packet[sizeof(rp)+1];
  memcpy(packet, &rp, sizeof(rp));
  byte checkSum = computeCheckSum(packet);
  packet[sizeof(packet)-1] = ~checkSum;

  //Envoi du packet sur le port serie
  Serial.write(packet, sizeof(packet));
  Serial.write("\n");
  /*
  for(int i = 0; i < 17; i++)
  {
    Serial.print(rp.array[i]);
    Serial.print(" ");
  }
  Serial.print("\n");
  */
  timestamp++;
  delay(200);
}
