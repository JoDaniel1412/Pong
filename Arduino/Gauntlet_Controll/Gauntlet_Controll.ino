#include<Wire.h>

// MPU settup
const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t GyX,GyY,GyZ;

// Buttons Variables
int red_button = 4;
int white_button = 5;
int blue_button = 6;
String p = "pause";
String st = "style";
String m = "mute";

String w = "w";
String s = "s";
String up = "up";
String down = "down";

void setup(){
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  Serial.begin(9600);
  pinMode(red_button, INPUT);
  pinMode(blue_button, INPUT);
  pinMode(white_button, INPUT);
}

void loop(){

  // Lectura del giroscopio
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
  GyX=Wire.read()<<8|Wire.read();  // Eje X del giroscopio
  GyY=Wire.read()<<8|Wire.read();  // Eje Y del giroscopio
  //GyZ=Wire.read()<<8|Wire.read();  // Eje Z del giroscopio
  //Serial.print(" | GyX = "); Serial.print(GyX);
  //Serial.print(" | GyY = "); Serial.println(GyY);
  //Serial.print(" | GyZ = "); Serial.println(GyZ);

  // Lectura de los botones
  int red_buttonState = digitalRead(red_button);
  int blue_buttonState = digitalRead(blue_button);
  int white_buttonState = digitalRead(white_button);

  if (red_buttonState == 0)  // Red Button
    Serial.println(st);    
    
  if (blue_buttonState == 0)  // Blue Button
    Serial.println(p);
    
  if (white_buttonState == 0)  // White Button
    Serial.println(m);    

  /*if (GyX < 0)  // Giroscopio W
    Serial.println(w); */
     
 /* if (GyX > 12000)  // Giroscopio S
    Serial.println(s); */ 

  if (GyY < 0)  // Giroscopio Up
    Serial.println(up); 
     
  if (GyY > 9000)  // Giroscopio Down
    Serial.println(down);  
  
  delay(100);
}
