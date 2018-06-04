char ser;
int pin = 11;
void setup() {
  pinMode(pin, OUTPUT);
  Serial.begin(9600);

}

void loop() {
  if(Serial.available() > 0){
    ser = Serial.read();
    Serial.print(ser);

    if(ser == '1'){
      digitalWrite(pin, HIGH);}
     else if(ser == '0'){
      digitalWrite(pin,LOW);}
    }
}


