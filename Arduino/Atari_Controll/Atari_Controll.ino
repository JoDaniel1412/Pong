//Down Leds Variables
#define ledVerde 3 
#define ledAzul 1
#define ledRojo 2
int contador = 0;

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
String w = "w";
String s = "s";

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

  pinMode(ledVerde, OUTPUT);
  pinMode(ledAzul, OUTPUT);
  pinMode(ledRojo, OUTPUT);

  // Inicia el contador en 0
  digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH); //0
}

void loop() {  
  //Encendido de Led inferiores
  contador += 1 ;
  if (contador % 60 == 0){
    digitalWrite(ledVerde, HIGH);//pone 5V en el pin (enciende el LED)
    digitalWrite(ledRojo, LOW);
  }
  else if (contador % 120 == 0){
    digitalWrite(ledAzul, HIGH);
   digitalWrite(ledVerde, LOW); 
  }
  else if (contador & 20 == 0){
    digitalWrite(ledRojo, HIGH);
    digitalWrite(ledAzul, LOW);
  }


  // Lectura del Joystick
  ejeY = analogRead(pinEjeY);
  ejeX = analogRead(pinEjeX);
  //Serial.print(ejeX); Serial.print("  "); Serial.println(ejeY);  // Impime los valores del Joystick  
  /*if (ejeX > 900)  // Eje X Joystick
    Serial.println(s); 
  if (ejeX < 700)  // Eje X Joystick
    Serial.println(w);*/
  if (ejeY < 700)  // Eje Y Joystick
    Serial.println(w);   
  if (ejeY > 900)  // Eje Y Joystick
    Serial.println(s); 


  // Lectura del potenciometro
  potenciometro = analogRead(pinPotenciometro);
  if (potenciometro > 1000)
    Serial.println(1);
  else if (potenciometro > 1000)
    Serial.println(1);
  else if (potenciometro > 900)
    Serial.println(0.7);
  else if (potenciometro > 800)
    Serial.println(0.5);
  else if (potenciometro > 700)
    Serial.println(0.3);
  else if (potenciometro < 700)
    Serial.println(0);

    
  // Lectura del contador
  data = Serial.read();
  if (data != -1){
    //Serial.println(data);
    if (data == 48){
    digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida7, LOW);digitalWrite(pinSalida10, LOW); //8
    digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH); //0
    }
    else if (data == 49){
    digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida7, LOW); //0
    digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida9, HIGH); //1
    }
    if (data == 50){
    digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida9, LOW); //1
    digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); //2
    }
    else if (data == 51){
    digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida12, LOW); //2
    digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida7, HIGH);  //3
    }
    else if (data == 52){
    digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida7, LOW);  //3
    digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida11, HIGH); //4
    }
    else if (data == 53){
    digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida13, LOW); digitalWrite(pinSalida11, LOW); //4
    digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); //5
    }
    else if (data == 54){
    digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida12, LOW); digitalWrite(pinSalida11, LOW); //5
    digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida10, HIGH); digitalWrite(pinSalida7, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida12, HIGH);//6
    }
    else if (data == 55){
    digitalWrite(pinSalida8, LOW); digitalWrite(pinSalida9, LOW); digitalWrite(pinSalida10, LOW); digitalWrite(pinSalida7, LOW); digitalWrite(pinSalida11, LOW); digitalWrite(pinSalida12, LOW);//6
    digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida9, HIGH); //7
    }
    else if (data == 56){
    digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida8, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH);digitalWrite(pinSalida10, HIGH); //8
    }
    else if (data == 57){
    digitalWrite(pinSalida8, LOW); //8
    digitalWrite(pinSalida9, HIGH); digitalWrite(pinSalida13, HIGH); digitalWrite(pinSalida12, HIGH); digitalWrite(pinSalida11, HIGH); digitalWrite(pinSalida7, HIGH);digitalWrite(pinSalida10, HIGH); //9
    }
  }
  delay(80);
}
