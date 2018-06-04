#define ledVerde 3 //definimos una constante con el pin que vamos a utilizar
#define ledAzul 1
#define ledRojo 2

void setup() {//Esta funcion solo se ejecuta una vez
  //Aca llamamos las funciones de configuracion (modo de pines, inicializar el puerto serial, etc...)
  pinMode(ledVerde, OUTPUT); //inicializamos el pin como una salida
  pinMode(ledAzul, OUTPUT);
  pinMode(ledRojo, OUTPUT);
}

void loop() {// Esta fucion se repite infinitamente
  digitalWrite(ledVerde, HIGH);
  delay(1000);
  digitalWrite(ledVerde, LOW);//pone 5V en el pin (enciende el LED)
  digitalWrite(ledAzul, HIGH);
  delay(1000);
  digitalWrite(ledAzul, LOW);                    
  digitalWrite(ledRojo, HIGH);
  delay(1000);
  digitalWrite(ledRojo, LOW);
}
