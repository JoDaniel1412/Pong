#define pinAnalogico A1
#define pinAnalogico1 A2
#define pinAnalogico2 A0
int lectura0 = 0;
int lectura1 = 1;
int lectura2 = 2;
void setup() {
  //inicializa la comunicacion serial
  Serial.begin(9600); //9600 es la "velocidad", el mismo valor debe ser seleccionado en el monitor serial
}

void loop() {
  lectura = analogRead(pinAnalogico); //leer el valor en el pin
  lectura1 = analogRead(pinAnalogico1);
  Serial.print("sensor = ");
  Serial.print(lectura2); // imprime el valor del sensor
  Serial.print(lectura1);
  Serial.println(lectura);
  delay(100); //espera para la siguiente lectura
}
