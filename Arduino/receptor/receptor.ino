//////////////////////////////////////////////////////////////////////////////////////
////////////////////      RECEPTOR      //////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////
#include <SPI.h>
#include "nRF24L01.h"
#include "RF24.h"

RF24 radio(9, 10); //Establezco los pines de CE y CS

const uint64_t pipe = { 0xF0F0F0F0E1LL}; //Pipe de comunicacion a usar. Puede ser cualquier cadena de 40-bits hexa. Tiene que ser la misma que la del receptor

void setup()
{
  pinMode(10, OUTPUT);
  Serial.begin(9600);
  radio.begin();
  radio.openReadingPipe(1, pipe); //Numero de pipe a abrir, pipe
  radio.startListe      |ning(); //Comienza a escuchar

}
void loop()
{
  int largoMensaje = 6;
  char mensaje[largoMensaje];
  if ( radio.available() )
  {
    radio.read(mensaje, largoMensaje);
    Serial.println(mensaje);
    delay(100);
  }
}
