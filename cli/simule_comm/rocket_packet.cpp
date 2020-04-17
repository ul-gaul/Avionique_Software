/*
 * rocket_packet.c
 *
 *  Created on: Nov 1, 2018
 *	  Author: laplace
 */

#include "rocket_packet.h"

unsigned int pack_avionics_data(AvionicsData* data, uint8_t* dst) {
	/*
	 * copy the rocket packet struct into the destination char array
	 */
	size_t offset = 0;
	char start_char = ROCKET_PACKET_START;

	// start char
	memcpy(dst + offset, (void *) &start_char, sizeof(char));
	offset += sizeof(char);
	// timestamp
	memcpy(dst + offset, (void *) &data->timestamp, sizeof(data->timestamp));
	offset += sizeof(data->timestamp);
	// GPS values
	memcpy(dst + offset, (void *) &data->latitude, sizeof(data->latitude));
	offset += sizeof(data->latitude);
	memcpy(dst + offset, (void *) &data->longitude, sizeof(data->longitude));
	offset += sizeof(data->longitude);
	memcpy(dst + offset, (void *) &data->NSIndicator, sizeof(data->NSIndicator));
	offset += sizeof(data->NSIndicator);
	memcpy(dst + offset, (void *) &data->EWIndicator, sizeof(data->EWIndicator));
	offset += sizeof(data->EWIndicator);
	memcpy(dst + offset, (void *) &data->UTCTime, sizeof(data->UTCTime));
	offset += sizeof(data->UTCTime);
	// 10DOF values
	memcpy(dst + offset, (void *) &data->altitude, sizeof(data->altitude));
	offset += sizeof(data->altitude);
	memcpy(dst + offset, (void *) &data->pressure, sizeof(data->pressure));
	offset += sizeof(data->pressure);
	memcpy(dst + offset, (void *) &data->temperature, sizeof(data->temperature));
	offset += sizeof(data->temperature);
	memcpy(dst + offset, (void *) &data->acc_x_uncomp, sizeof(data->acc_x_uncomp));
	offset += sizeof(data->acc_x_uncomp);
	memcpy(dst + offset, (void *) &data->acc_y_uncomp, sizeof(data->acc_y_uncomp));
	offset += sizeof(data->acc_y_uncomp);
	memcpy(dst + offset, (void *) &data->acc_z_uncomp, sizeof(data->acc_z_uncomp));
	offset += sizeof(data->acc_z_uncomp);
	memcpy(dst + offset, (void *) &data->acc_x, sizeof(data->acc_x));
	offset += sizeof(data->acc_x);
	memcpy(dst + offset, (void *) &data->acc_y, sizeof(data->acc_y));
	offset += sizeof(data->acc_y);
	memcpy(dst + offset, (void *) &data->acc_z, sizeof(data->acc_z));
	offset += sizeof(data->acc_z);
	memcpy(dst + offset, (void *) &data->mag_x, sizeof(data->mag_x));
	offset += sizeof(data->mag_x);
	memcpy(dst + offset, (void *) &data->mag_y, sizeof(data->mag_y));
	offset += sizeof(data->mag_y);
	memcpy(dst + offset, (void *) &data->mag_z, sizeof(data->mag_z));
	offset += sizeof(data->mag_z);
	memcpy(dst + offset, (void *) &data->x_gyro, sizeof(data->x_gyro));
	offset += sizeof(data->x_gyro);
	memcpy(dst + offset, (void *) &data->y_gyro, sizeof(data->y_gyro));
	offset += sizeof(data->y_gyro);
	memcpy(dst + offset, (void *) &data->z_gyro, sizeof(data->z_gyro));
	offset += sizeof(data->z_gyro);

	return offset;
}

unsigned int pack_command_packet(CommandPacket* pkt, uint8_t* dst) {
	unsigned int offset = 0;
	
	memcpy(dst + offset, (void *) &pkt->start_short, sizeof(pkt->start_short));
	offset += sizeof(pkt->start_short);

	memcpy(dst + offset, (void *) &pkt->id, sizeof(pkt->id));
	offset += sizeof(pkt->id);
	
	memcpy(dst + offset, (void *) &pkt->function, sizeof(pkt->function));
	offset += sizeof(pkt->function);
	
	memcpy(dst + offset, (void *) &pkt->arg, sizeof(pkt->arg));
	offset += sizeof(pkt->arg);
	
	memcpy(dst + offset, (void *) &pkt->crc, sizeof(pkt->crc));
	offset += sizeof(pkt->crc);
	
	return offset;
}


unsigned int unpack_command_packet(CommandPacket* pkt, uint8_t* src) {
	unsigned int offset = 0;

	memcpy((void *) &pkt->start_short, src + offset, sizeof(pkt->start_short));
	offset += sizeof(pkt->start_short);

	memcpy((void *) &pkt->id, src + offset, sizeof(pkt->id));
	offset += sizeof(pkt->id);

	memcpy((void *) &pkt->function, src + offset, sizeof(pkt->function));
	offset += sizeof(pkt->function);

	memcpy((void *) &pkt->arg, src + offset, sizeof(pkt->arg));
	offset += sizeof(pkt->arg);

	memcpy((void *) &pkt->crc, src + offset, sizeof(pkt->crc));
	offset += sizeof(pkt->crc);

	return offset;
}

unsigned int pack_ack_packet(AckPacket* pkt, uint8_t* dst) {
	unsigned int offset = 0;
	
	memcpy(dst + offset, (void *) &pkt->start_short, sizeof(pkt->start_short));
	offset += sizeof(pkt->start_short);

	memcpy(dst + offset, (void *) &pkt->id, sizeof(pkt->id));
	offset += sizeof(pkt->id);
	
	memcpy(dst + offset, (void *) &pkt->ack, sizeof(pkt->ack));
	offset += sizeof(pkt->ack);
	
	memcpy(dst + offset, (void *) &pkt->crc, sizeof(pkt->crc));
	offset += sizeof(pkt->crc);
	
	return offset;
}


unsigned int unpack_ack_packet(AckPacket* pkt, uint8_t* src) {
	unsigned int offset = 0;

	memcpy((void *) &pkt->start_short, src + offset, sizeof(pkt->start_short));
	offset += sizeof(pkt->start_short);

	memcpy((void *) &pkt->id, src + offset, sizeof(pkt->id));
	offset += sizeof(pkt->id);

	memcpy((void *) &pkt->ack, src + offset, sizeof(pkt->ack));
	offset += sizeof(pkt->ack);

	memcpy((void *) &pkt->crc, src + offset, sizeof(pkt->crc));
	offset += sizeof(pkt->crc);

	return offset;
}
