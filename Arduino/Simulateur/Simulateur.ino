#include "rocketData.h"
#include "rocketData18.h"
#include "rocketData19.h"

#define START_BYTE 's'
#define ROCKET_PACKET_VERSION 2019
#define BAUDRATE 9600

int timestamp = 0;
RocketPacket rp17;
RocketPacket18 rp18;
RocketPacket19 rp19;

void writeToSerial(void* data, size_t numBytes)
{
  Serial.write(START_BYTE);
  Serial.write((byte*)data, numBytes);
}

void setup()
{
  // put your setup code here, to run once:
  Serial.begin(BAUDRATE);
}

void loop()
{
  switch (ROCKET_PACKET_VERSION) {
    case 2017:
      createRocketPacket2017(rp17, timestamp);
      writeToSerial(&rp17, sizeof(RocketPacket));
      break;
    case 2018:
      createRocketPacket2018(rp18, timestamp);
      writeToSerial(&rp18, sizeof(RocketPacket18));
      break;
    case 2019:
      createRocketPacket2019(rp19, timestamp);
      writeToSerial(&rp19, sizeof(RocketPacket19));
      break;
  }

  timestamp++;
  delay(1000 * (1.0 / FREQUENCY));
}
