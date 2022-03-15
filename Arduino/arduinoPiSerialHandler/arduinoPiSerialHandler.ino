//////////////////////////////////////////////////////////////////////////////////////////
//
//    |Max32664 pin label| Arduino Connection  |Pin Function      |
//    |----------------- |---------------------|------------------|
//    | SDA              | A4                  |  Serial Data     |
//    | SCL              | A5                  |  Serial Clock    |
//    | Vin              | 5V                  |  Power           |
//    | GND              | Gnd                 |  Gnd             |
//    | MFIO Pin         | 02                  |  MFIO            |
//    | RESET Pin        | 04                  |  Reset           |
//    |-----------------------------------------------------------|
//
/////////////////////////////////////////////////////////////////////////////////////////

#include <Wire.h>
#include "max32664.h"
#include <Adafruit_MLX90614.h>

#define RESET_PIN 04
#define MFIO_PIN 02
#define RAWDATA_BUFFLEN 250

bool sensorEnable = false;

//Initialize pins for MAX32664 HR and BP sensor
max32664 MAX32664(RESET_PIN, MFIO_PIN, RAWDATA_BUFFLEN);
//Initialize MLX90614 temp sensor
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

//MAX32664 required functions
void mfioInterruptHndlr(){
  //Serial.println("i");
}

void enableInterruptPin(){

  //pinMode(mfioPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(MAX32664.mfioPin), mfioInterruptHndlr, FALLING);

}

void loadAlgomodeParameters(){

  algomodeInitialiser algoParameters;
  /*  Replace the predefined values with the calibration values taken with a reference spo2 device in a controlled environt.
      Please have a look here for more information, https://pdfserv.maximintegrated.com/en/an/an6921-measuring-blood-pressure-MAX32664D.pdf
      https://github.com/Protocentral/protocentral-pulse-express/blob/master/docs/SpO2-Measurement-Maxim-MAX32664-Sensor-Hub.pdf
  */

  algoParameters.calibValSys[0] = 120;
  algoParameters.calibValSys[1] = 122;
  algoParameters.calibValSys[2] = 125;

  algoParameters.calibValDia[0] = 80;
  algoParameters.calibValDia[1] = 81;
  algoParameters.calibValDia[2] = 82;

  algoParameters.spo2CalibCoefA = 1.5958422;
  algoParameters.spo2CalibCoefB = -34.659664;
  algoParameters.spo2CalibCoefC = 112.68987;

  MAX32664.loadAlgorithmParameters(&algoParameters);
}

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
