//Down Leds Variables
#define ledVerde 3 
#define ledAzul 1
#define ledRojo 2
int contador = 0 ;

// Counter Variables
#define pinSalida7 7
#define pinSalida8 8 
#define pinSalida9 9
#define pinSalida10 10
#define pinSalida11 11
#define pinSalida12 12
#define pinSalida13 13
int data;

// Analogic Variables
#define pinPotenciometro A0
#define pinEjeY A1
#define pinEjeX A2
int potenciometro;
int ejeY;
int ejeX;

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

void setup() {

  // Inicializa los pines
  Serial.begin(9600);
  pinMode(pinSalida7, OUTPUT);  
  pinMode(pinSalida8, OUTPUT); 
  pinMode(pinSalida9, OUTPUT); 
  pinMode(pinSalida10, OUTPUT);
  pinMode(pinSalida11, OUTPUT); 
  pinMode(pinSalida12, OUTPUT);
  pinMode(pinSalida13, OUTPUT);
/*
  pinMode(red_button, INPUT);
  pinMode(blue_button, INPUT);
  pinMode(white_button, INPUT);
*/

  pinMode(ledVerde, OUTPUT); //inicializamos el pin como una salida
  pinMode(ledAzul, OUTPUT);
  pinMode(ledRojo, OUTPUT);
}

void loop() {// Esta fucion se repite infinitamente

  //Encendido de Led inferiores
  contador += 1 ;
  if (contador % 60 == 0){
    digitalWrite(ledVerde, HIGH);//pone 5V en el pin (enciende el LED)
    digitalWrite(ledRojo, LOW);
  }
  if (contador % 120 == 0){
    digitalWrite(ledAzul, HIGH);
   digitalWrite(ledVerde, LOW); 
  }
  if (contador % 20 == 0){
    digitalWrite(ledRojo, HIGH);
    digitalWrite(ledAzul, LOW);
  }

  // Lectura de los analogicos
  ejeY = analogRead(pinEjeY);
  ejeX = analogRead(pinEjeX);
  potenciometro = analogRead(pinPotenciometro);
  String potenciometroString = "P%" + String(potenciometro);
  Serial.println(potenciometroString);

  if (ejeX > 650)  // Eje X Joystick
    Serial.println(s); 

  if (ejeX < 350)  // Eje X Joystick
    Serial.println(w); 
    
  if (ejeY > 650)  // Eje Y Joystick
    Serial.println(s); 

  if (ejeY < 350)  // Eje Y Joystick
    Serial.println(w); 
    
  /*// Lectura de los botones
  int red_buttonState = digitalRead(red_button);
  int blue_buttonState = digitalRead(blue_button);
  int white_buttonState = digitalRead(white_button);

  if (blue_buttonState == 1)  // Blue Button
    Serial.println(p);    
  */
  // Lectura del contador
  data = Serial.read();
  Serial.println(data);
  if (data == 48){
  digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida7, LOW);digitalWrite(pinSalida10, LOW); //8
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH); //0
  }
  if (data == 49){
  digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida7, LOW); //0
  digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida9, HIGH); //1
  }
  if (data == 50){
  digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida9, LOW); //1
  digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); //2
  }
  if (data == 51){
  digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); //2
  digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida7, HIGH);  //3
  }
  if (data == 52){
  digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida7, LOW);  //3
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida11, HIGH); //4
  }
  if (data == 53){
  digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida11, LOW); //4
  digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); //5
  }
  if (data == 54){
  digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); //5
  digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida12, HIGH);//6
  }
  if (data == 55){
  digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida12, LOW);//6
  digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida9, HIGH); //7
  }
  if (data == 56){
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH);digitalWrite(pinSalida10, HIGH); //8
  }
  if (data == 57){
  digitalWrite(pinSalida8, LOW); //8
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH);digitalWrite(pinSalida10, HIGH); //9
  }

  delay(100);
}
