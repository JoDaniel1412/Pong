#include<Wire.h>

// MPU settup
const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t GyX,GyY,GyZ;

// Buttons Variables
int red_button = 4;
int white_button = 5;
int blue_button = 6;
#define pinSalida7 7
#define pinSalida8 8 
#define pinSalida9 9
#define pinSalida10 10
#define pinSalida11 11
#define pinSalida12 12
#define pinSalida13 13
int data;
String p = "pause";
String st = "style";
String m = "mute";

String w = "w";
String s = "s";

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
    Serial.println(w); 
     
  if (GyY > 9000)  // Giroscopio Down
    Serial.println(s);

  // Lectura del contador
  data = Serial.read();
  Serial.println(data);
  if (data == 48){
  digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida7, LOW);digitalWrite(pinSalida10, LOW); //8
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH); //0
  }
  if (data == 49){
  digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida10, LOW); //0
  digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH); //1
  }
  if (data == 50){
  digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida7, LOW); //1
  digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); //2
  }
  if (data == 51){
  digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); //2
  digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH);  //3
  }
  if (data == 52){
  digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW);  //3
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida11, HIGH); //4
  }
  if (data == 53){
  digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida11, LOW); //4
  digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); //5
  }
  if (data == 54){
  digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); //5
  digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida12, HIGH);//6
  }
  if (data == 55){
  digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida12, LOW);//6
  digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida11, HIGH); //7
  }
  if (data == 56){
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH);digitalWrite(pinSalida10, HIGH); //8
  }
  if (data == 57){
  digitalWrite(pinSalida13, LOW); //8
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH);digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida8, HIGH); //9
  }

  delay(100);
}
