int boton = 6;
int boton1 = 5;//evitar usar pines 0 y 1
int boton2 = 4;
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
  //inicializa la comunicacion serial
  Serial.begin(9600); //9600 es la "velocidad", el mismo valor debe ser seleccionado en el monitor serial
  pinMode(boton, INPUT);//declaramos el pin como una entrada digital (HIGH o LOW, 0 o 5V)
  pinMode(boton1, INPUT);
  pinMode(boton2, INPUT);
}

void loop() {
  int buttonState = digitalRead(boton); //lee el estado del pin (0 o 1, 0 o 5v)
  int buttonState2 = digitalRead(boton1);
  int buttonState3 = digitalRead(boton2);
  String buttonOUT = "B1%"+ String(buttonState);
  String button1OUT = "B2%"+ String(buttonState2);
  String button2OUT = "B3&" + String(buttonState3);
  Serial.println(buttonOUT);
  Serial.println(button1OUT);
  Serial.println(button2OUT);
  delay(100);        // espera para la siguiente lectura
}
