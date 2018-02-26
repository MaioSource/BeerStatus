#include <OneWire.h> //Se importan las librerías
#include <DallasTemperature.h>
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

#define Pin 2 //Se declara el pin donde se conectará la DATA


RF24 radio(9, 10); //Establezco los pines de CE y CS
const uint64_t pipe = { 0xF0F0F0F0E1LL}; //Pipe de comunicacion a usar. Puede ser cualquier cadena de 40-bits hexa. Tiene que ser la misma que la del receptor

OneWire ourWire(Pin); //Se establece el pin declarado como bus para la comunicación OneWire
 
DallasTemperature sensors(&ourWire); //Se instancia la librería DallasTemperature
 
void setup() {
delay(1000);
pinMode(10, OUTPUT);
radio.begin();
radio.setRetries(15, 15); //Si falla el envio, lo vuelve a mandar en <delay, contador> (Cuanto espera, cuantos intentos)
//radio.setPayloadSize(8); //Cambia el tamaño maximo de los datos a enviar (Por defecto 32 bytes)
radio.openWritingPipe(pipe); //Abre el pipe de comunicacion
radio.setPALevel(RF24_PA_MAX); 
Serial.begin(9600);
sensors.begin(); //Se inician los sensores
}
 
void loop() {
sensors.requestTemperatures(); //Prepara el sensor para la lectura

float temperature = sensors.getTempCByIndex(0);
Serial.print(temperature); //Se lee e imprime la temperatura en grados Celsius
int largoMensaje = 5;
char result[largoMensaje]; 
dtostrf(temperature, 6, 2, result); // Leave room for too large numbers!
Serial.print("RESULT: ");
Serial.println(result);
radio.write(result, largoMensaje);
Serial.println(" Enviado");
delay(1000); //Se provoca un lapso de 1 segundo antes de la próxima lectura
}

