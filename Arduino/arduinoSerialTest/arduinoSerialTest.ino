//////////////////////////////////////////////////////////////////////////////////////////
//
//    Demo code for the protoCentral MAX32664 breakout board
//
//    Author: Joice Tm
//    Copyright (c) 2020 ProtoCentral
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
//    This software is licensed under the MIT License(http://opensource.org/licenses/MIT).
//
//    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
//    NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
//    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
//    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
//    SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//
/////////////////////////////////////////////////////////////////////////////////////////


#include <Wire.h>
#include "max32664.h"
#include <Adafruit_MLX90614.h>

#define RESET_PIN 04
#define MFIO_PIN 02
#define RAWDATA_BUFFLEN 250

max32664 MAX32664(RESET_PIN, MFIO_PIN, RAWDATA_BUFFLEN);
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

int sensorEnable = 0;

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

void tempSensorStartup(){
  //MLX temperature sensor startup
  Serial.println("Entered MLX startup function");
  if (!mlx.begin()) {
    Serial.println("Error connecting to MLX sensor. Check wiring.");
  }else{
    Serial.println("Temp sensor started successfully");
  };
}

void hrBpSensorStartup(){
  //MAX heart rate and blood pressure sensor startup
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

    delay(10000);
    Serial.println("failed calib, please restart");
    //ret = MAX32664.startBPTcalibration();
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

void setup(){

  Serial.begin(57600);
  Wire.begin();

  while(1){
    if(Serial.available() > 0){
    sensorEnable = Serial.parseInt();
      if(sensorEnable){
        Serial.println("Enable signal received");
        tempSensorStartup();
        hrBpSensorStartup();
        break;
      }
      Serial.println("Sensor enable signal not received");
    }
    Serial.println("No serial connection available");
  }
}

void loop(){

  //MLX loop
  Serial.print("Ambient = "); Serial.print(mlx.readAmbientTempC());
  Serial.print("*C\tObject = "); Serial.print(mlx.readObjectTempC()); Serial.println("*C");

  //MAX loop
  uint8_t num_samples = MAX32664.readSamples();

  if(num_samples){

    Serial.print("hr = ");
    Serial.print(MAX32664.max32664Output.hr);
    Serial.print(", sys = ");
    Serial.print(MAX32664.max32664Output.sys);
    Serial.print(", dia = ");
    Serial.print(MAX32664.max32664Output.dia);
    Serial.println();
  }

  delay(500);
}
