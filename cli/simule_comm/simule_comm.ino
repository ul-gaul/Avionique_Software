#include "rocket_packet.h"
#include "crc.h"


CommandPacket cmd;
AckPacket ack;
char cmdbuf[CMD_PACKET_SIZE];
char ackbuf[ACK_PACKET_SIZE];
crc_t crc;


void setup() {
	/* init serial bus */
	Serial.begin(115200);
}


void loop() {
	/* init the crc */
	crc = crc_init();

	/* recoit le Cmdpacket */
	if (Serial.available() >= CMD_PACKET_SIZE) {
		Serial.readBytes(cmdbuf, CMD_PACKET_SIZE);
	} else {
		/* skip to next call of loop() */
		return;
	}

	Serial.print("received string:");
	Serial.write(cmdbuf, CMD_PACKET_SIZE);
	Serial.print("\n");

	/* calcul le crc */
	crc = crc_update(crc, cmdbuf, CMD_PACKET_SIZE);

	crc = crc_finalize(crc);

	if (crc != 0) {
		ack.ack = NACK;
	} else {
		ack.ack = ACK;
	}

	// SI CRC == 0 TODO
	unpack_command_packet(&cmd, (unsigned char *) cmdbuf);

	/* wait 0.1 sec to simulate sending the command to the motor control unit */
	delay(100);

	ack.start_short = COMMAND_START;
	ack.id = cmd.id;
	ack.crc = 0;

	/* simulate command failing with probability 0.1 */
	if (random(0, 1) < 0.1) {
		ack.ack = NACK;
	}
	
	// il faut Serialliser le Ack packet dans le ack bufur
	pack_ack_packet(&ack, (unsigned char *) ackbuf);

	/* compute crc on buffer and append to ack packet */
	crc = crc_init();
	crc = crc_update(crc, ackbuf, ACK_PACKET_SIZE);
	ack.crc = crc_finalize(crc);
	pack_ack_packet(&ack, (unsigned char *) ackbuf);

	/* send back acknowledge packet */ 
	Serial.write(ackbuf, ACK_PACKET_SIZE);
}

