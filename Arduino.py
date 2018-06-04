import serial
import time
ser = serial.Serial('COM6', 9600)


def leerPotenciometro():
    while True:
        try:
            entrada = str(ser.readline())
            datos = entrada[entrada.index("'")+1: entrada.index("\\")]
            datos = int(datos[9:])/1000
            print(datos, 'Este es el dato 1')
        except:
           pass


def leerBotones():
    while True:
        try:
            entrada = str(ser.readline())
            datos = entrada[entrada.index("'")+1: entrada.index("\\")]
            return datos
        except:
           pass

def leerArduino():
        try:
            entrada = str(ser.readline())
            datos = entrada[entrada.index("'")+1: entrada.index("\\")]
            return datos
        except:
            pass

while 1:
    datos = leerArduino()
    print(datos)