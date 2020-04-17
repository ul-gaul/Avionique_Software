/*
 * rocket_packet.h
 *
 *  Created on: Nov 1, 2018
 *      Author: laplace
 */

#include <stdint.h>
#include <string.h>


#ifndef _ROCKET_PACKET_H_
#define _ROCKET_PACKET_H_

#define ROCKET_PACKET_START 's'

#define ACK_PACKET_SIZE 7

#define CMD_PACKET_SIZE 8

#define AVIONICS_DATA_SIZE 76

#define MOTOR_DATA_SIZE 18

#define ROCKET_PACKET_SIZE (AVIONICS_DATA_SIZE \
                            + MOTOR_DATA_SIZE \
                            + 3)

#define COMMAND_START 0xface

#define ACK 0x01
#define NACK 0xff


typedef struct {
	/* time since boot in milliseconds */
	double timestamp;
	/* GPS values */
	double latitude;
	double longitude;
	char NSIndicator;
	char EWIndicator;
	double UTCTime;
	/*
	 * 10DOF values
	 * BMP180
	 */
	float altitude;
	uint32_t pressure;
	float temperature;
	/*
	 * lsm303
	 * acceleration values are in milli-G
	 * magnetic field values are in milli-gauss
	 */
	int16_t acc_x_uncomp;
	int16_t acc_y_uncomp;
	int16_t acc_z_uncomp;
	float acc_x;
	float acc_y;
	float acc_z;
	int16_t mag_x;
	int16_t mag_y;
	int16_t mag_z;
	/*
	 * l3dg20
	 * angular speed values are in degrees/s
	 */
	int16_t x_gyro;
	int16_t y_gyro;
	int16_t z_gyro;
} AvionicsData;

typedef struct {
	/* TODO: fix types and array sizes */
	uint8_t valve_states[5];
	uint8_t piston_state;
	uint16_t manometers[5];
	uint16_t piezoelectric;
} MotorData;

typedef struct {
	AvionicsData avionics_data;
	MotorData motor_data;
	char start_char;
	uint16_t crc;
} RocketPacket;

typedef struct {
	uint16_t start_short;
	uint16_t id;
	uint8_t function;
	uint8_t arg;
	uint16_t crc;
} CommandPacket;

typedef struct {
	uint16_t start_short;
	uint16_t id;
	uint8_t ack;
	uint16_t crc;
} AckPacket;


/*
 * Serialize the rocket packet for transmission.
 */
unsigned int pack_rocket_packet(RocketPacket* pkt, uint8_t* dst);

unsigned int pack_avionics_data(AvionicsData* data, uint8_t* dst);

unsigned int pack_motor_data(MotorData* data, uint8_t* dst);

unsigned int pack_command_packet(CommandPacket* pkt, uint8_t* dst);

unsigned int pack_ack_packet(AckPacket* pkt, uint8_t* dst);

unsigned int unpack_ack_packet(AckPacket* pkt, uint8_t* src);

unsigned int unpack_command_packet(CommandPacket* pkt, uint8_t* src);

#endif /* _ROCKET_PACKET_H_ */
