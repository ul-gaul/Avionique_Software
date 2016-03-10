

/*
  
  Serial Call and Response
  Language : Wiring/Arduino
  
  This program sends and ASCII A (bye of value 65) on startup
  and repeats that until it gets some data in.
  Then it waits for a byte in the serial port, and
  send three sensor values whenever it gets a byte in.
  
 */
 
int firstSensor = 0;
int sndSensor = 0;
int thirdSensor = 0; 
int inByte = 0;
 
void setup(){
   
  Serial.begin(9600);
  while (!Serial) {
    ;
  }
  pinMode(2, INPUT);
  establishContact();
}
 
void loop() {
   
  if (Serial.available() > 0) {
    inByte = Serial.read();
    firstSensor = analogRead(A0)/4;
    sndSensor = analogRead(1)/4
    thirdSensor = map(digitalRead(2), 0, 1, 0, 255);
    Serial.write(firstSensor);
    Serial.write(sndSensor);
    Serial.write(thirdSensor);
  }
}
 
void establishContact() {
  while (Serial.available() <= 0){
    Serial.print('A');
    delay(300);
  }
}
