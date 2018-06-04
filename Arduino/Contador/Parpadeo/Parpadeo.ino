#define pin11 11 //definimos una constante con el pin que vamos a utilizar
#define pin7 7
#define pin8 8
#define pin9 9
#define pin10 10
#define pin12 12
#define pin13 13
#define delai 1000

void setup() {//Esta funcion solo se ejecuta una vez
  //Aca llamamos las funciones de configuracion (modo de pines, inicializar el puerto serial, etc...)
  pinMode(pin11, OUTPUT); pinMode(pin7, OUTPUT); pinMode(pin8, OUTPUT); pinMode(pin9, OUTPUT); pinMode(pin10, OUTPUT); pinMode(pin11, OUTPUT); pinMode(pin12, OUTPUT); pinMode(pin13, OUTPUT);
}

void loop() {// Esta fucion se repite infinitamente
  /*Siete segmentos, numero 1 */
  digitalWrite(pin10, HIGH); digitalWrite(pin7, HIGH); delay(1000);     
  digitalWrite(pin10, LOW); digitalWrite(pin7, LOW);

  /*Siete segmentos, numero 2 */
  digitalWrite(pin11, HIGH); digitalWrite(pin10, HIGH); digitalWrite(pin8, HIGH);digitalWrite(pin9, HIGH); digitalWrite(pin13, HIGH);delay(delai);           
  digitalWrite(pin11, LOW); digitalWrite(pin10, LOW); digitalWrite(pin8, LOW); digitalWrite(pin9, LOW); digitalWrite(pin13, LOW);

  /*Siete segmentos, numero 3 */
  digitalWrite(pin11, HIGH); digitalWrite(pin10, HIGH); digitalWrite(pin7, HIGH);digitalWrite(pin8, HIGH);digitalWrite(pin13, HIGH);delay(delai);
  digitalWrite(pin11, LOW); digitalWrite(pin10, LOW); digitalWrite(pin7, LOW); digitalWrite(pin8, LOW); digitalWrite(pin13, LOW);

  /*Siete segmentos, numero 4 */
  digitalWrite(pin10, HIGH); digitalWrite(pin7, HIGH); digitalWrite(pin12, HIGH);digitalWrite(pin13, HIGH);delay(delai);
  digitalWrite(pin11, LOW); digitalWrite(pin10, LOW); digitalWrite(pin7, LOW);digitalWrite(pin13, LOW);

  /*Siete segmentos, numero 5 */
   digitalWrite(pin11, HIGH); digitalWrite(pin7, HIGH); digitalWrite(pin8, HIGH); digitalWrite(pin12, HIGH); digitalWrite(pin13, HIGH);delay(delai);
   digitalWrite(pin11, LOW); digitalWrite(pin10, LOW); digitalWrite(pin8, LOW); digitalWrite(pin12, LOW); digitalWrite(pin13, LOW);

   /*Siete segmentos, numero 6 */
   digitalWrite(pin11, HIGH); digitalWrite(pin7, HIGH); digitalWrite(pin8, HIGH);digitalWrite(pin9, HIGH); digitalWrite(pin12, HIGH); digitalWrite(pin13, HIGH);delay(delai);
   digitalWrite(pin11, LOW); digitalWrite(pin7, LOW); digitalWrite(pin8, LOW);digitalWrite(pin9, LOW); digitalWrite(pin12, LOW); digitalWrite(pin13, LOW);

    /*Siete segmentos, numero 7 */
   digitalWrite(pin11, HIGH); digitalWrite(pin10, HIGH); digitalWrite(pin7, HIGH);delay(delai);
   digitalWrite(pin11, LOW); digitalWrite(pin10, LOW); digitalWrite(pin7, LOW);

    /*Siete segmentos, numero 8 */
  digitalWrite(pin11, HIGH); digitalWrite(pin10, HIGH); digitalWrite(pin7, HIGH); digitalWrite(pin12, HIGH); digitalWrite(pin8, HIGH); digitalWrite(pin9, HIGH);digitalWrite(pin13, HIGH);delay(delai);
  digitalWrite(pin11, LOW); digitalWrite(pin10, LOW); digitalWrite(pin7, LOW);digitalWrite(pin12, LOW);digitalWrite(pin9, LOW); digitalWrite(pin8, LOW); digitalWrite(pin13, LOW);

    /*Siete segmentos, numero 9 */
  digitalWrite(pin11, HIGH); digitalWrite(pin10, HIGH); digitalWrite(pin7, HIGH); digitalWrite(pin12, HIGH); digitalWrite(pin8, HIGH);digitalWrite(pin13, HIGH);delay(delai);
  digitalWrite(pin11, LOW); digitalWrite(pin10, LOW); digitalWrite(pin7, LOW);digitalWrite(pin12, LOW); digitalWrite(pin8, LOW); digitalWrite(pin13, LOW);

  
}
