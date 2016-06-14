void setup() 
{
  Serial.begin(9600); //set the baudrate
  //Serial.print("Ready\n"); //print ready once
}

void loop() 
{
  float sensorValue = analogRead(A0);
  float voltage = 5*sensorValue/1023;
  Serial.println(voltage);

  //int sensorValue = analogRead(A0);
  //Serial.write(sensorValue);
  //Serial.write(64);
  delay(100);
} 
