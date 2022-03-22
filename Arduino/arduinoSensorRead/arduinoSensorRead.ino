/*
 * serial_usb_simple_arduino - For communicating over USB serial. Send it a '1' (character one) 
 * and it will make the builtin LED start blinking every one second. Send it a '0' 
 * (character zero) and it will make it stop blinking.
 * 
 * Each time it receives one of the commands, it sends back an 'A' for acknowledge.
 * But send it a commmand it doesn't recognize and it sends back an 'E' for error.
 */
#include <Wire.h>
#include "max32664.h"
#include <Adafruit_MLX90614.h>

#define RESET_PIN 04
#define MFIO_PIN 02
#define RAWDATA_BUFFLEN 250

max32664 MAX32664(RESET_PIN, MFIO_PIN, RAWDATA_BUFFLEN);
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

bool sensorEnable = false;

//----------------------------------------------------------
//MAX32664 setup functions
//----------------------------------------------------------
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

//----------------------------------------------------------
//MAX32664 startup function
//----------------------------------------------------------
void hrBpSensorStartup(){
  loadAlgomodeParameters();

  int result = MAX32664.hubBegin();
  if (result == CMD_SUCCESS){
    Serial.println("Sensorhub begin!");
  }else{
    //stay here.
    while(1){
      Serial.println("Could not communicate with the sensor! please make proper connections");
      delay(5000);
    }
  }

  bool ret = MAX32664.startBPTcalibration();
  while(!ret){

    delay(5000);
    Serial.println("Failed calibration, restarting calibration");
    ret = MAX32664.startBPTcalibration();
  }

  delay(1000);

  //Serial.println("start in estimation mode");
  ret = MAX32664.configAlgoInEstimationMode();
  while(!ret){

    Serial.println("Failed estimation mode");
    ret = MAX32664.configAlgoInEstimationMode();
    delay(10000);
  }

  //MAX32664.enableInterruptPin();
  Serial.println("Getting the device ready..");
  delay(1000);
}

//----------------------------------------------------------
//MLX90614 startup function
//----------------------------------------------------------
void tempSensorStartup(int action){
  Serial.println("Entered MLX startup function");
  if (!mlx.begin()) {
    Serial.println("Error connecting to MLX sensor. Check wiring.");
  }else{
    //If start measure was pressed
    if(action == 0){
      Serial.println("Temp sensor started successfully");
    } else if(action == 1){
      Serial.println("Temp sensor recalibrated successfully");
    }
  };
}

void setSensorEnable(bool val){
  sensorEnable = val;
}

bool getSensorEnable(){
  return sensorEnable;
}


void setup() {
  Serial.begin(57600);
  Wire.begin();
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}

void loop() {
  char c;
  
  if (Serial.available() > 0) {
    c = Serial.read();
    switch (c) {
    //Run sensor startup routines
    case '0':
      tempSensorStartup(0);
      hrBpSensorStartup();
      setSensorEnable(true);
      Serial.write("A", 1);
      break;
    //restart sensors to recalibrate them
    case '1':
      setSensorEnable(false);
      tempSensorStartup(1);
      hrBpSensorStartup();
      setSensorEnable(true);
      Serial.write("A", 1);
      break;
    default:
      Serial.write("E", 1);
      printf("Error");
      break;    
    }
    
  }
    //Send sensor values to Pi only if sensors have been enabled. This is triggered by 
    //pressing the 'start measuring' button on the gui in the Pi
    //bool sensorCheck = getSensorEnable();
    uint8_t num_samples = MAX32664.readSamples();
    if (sensorEnable && num_samples){
      //Notify Pi that sensor data is about to be sent
      Serial.write("T", 1);
      //Comma separated sensor values: temp, hr, dia, sys 
      Serial.print(mlx.readObjectTempC());
      Serial.print(",");
      Serial.print(MAX32664.max32664Output.hr);
      Serial.print(",");
      Serial.print(MAX32664.max32664Output.sys);
      Serial.print(",");
      Serial.println(MAX32664.max32664Output.dia);
    } 

    delay(100);
}
