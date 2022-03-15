/*
 * serial_usb_simple_arduino - For communicating over USB serial. Send it a '1' (character one) 
 * and it will make the builtin LED start blinking every one second. Send it a '0' 
 * (character zero) and it will make it stop blinking.
 * 
 * Each time it receives one of the commands, it sends back an 'A' for acknowledge.
 * But send it a commmand it doesn't recognize and it sends back an 'E' for error.
 */

void setup() {
  Serial.begin(57600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB
  }
}

void loop() {
  char c;
  
  if (Serial.available() > 0) {
    c = Serial.read();
    switch (c) {
    case '0':
      // stop blinking
      printf("Stop blinking");
      Serial.write("A", 1);
      break;
    case '1':
      // start blinking
      printf("start blinking");
      Serial.write("A", 1);
      break;
    default:
      Serial.write("E", 1);
      printf("Error");
      break;    
    }
  } 
}
