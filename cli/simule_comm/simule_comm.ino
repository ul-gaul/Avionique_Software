#include <rocket_packet.h>

CommandPacket cmd;
AckPacket ack;
char cmdbuffe[CMD_PACKET_SIZE];
char ackbuffe[ACK_PACKET_SIZE];



void setup() {
  // put your setup code here, to run once:
Serial.begin(115200);
}

void loop() {
  /*recoit le Cmdpacket*/
  if (Serial.available() >= CMD_PACKET_SIZE) {
    Serial.readBytes(cmdbuffe, CMD_PACKET_SIZE);
    
  } 
  else 
  {
    return;
  }
  //calcul le crc TODO 
  //si CRC != 0* renvoyer le ack.ack =NACK (NACK = 0xFF) TODO/*
 // SI CRC == 0 TODO  
 unpack_command_packet(&cmd, cmdbuffe);
 //attend 0.1s 
 delay(100);

  //x = random();
  // x entre 0 et 1
   
  ack.start_short = COMMAND_START;
  ack.id = cmd.id;
  ack.crc = 0;
  //si x> 0.1
  //ack.ack = ACK
  if (random(0, 1) >= 0.1){
    ack.ack = ACK;
  }
  else
  {
    ack.ack = NACK;
  }
  
   // il faut Serialliser le Ack packet dans le ack buffeur
  pack_ack_packet(&ack, ackbuffe);
   // calculer le crc sur buffeur

   // envoyer le buffeur 
  Serial.write(ackbuffe, ACK_PACKET_SIZE);


}
