/*

Executive part of the solar tracker project.

  - The Y servo is a controlled object.
  - The X servo is a static object - it is used to rigidly hold the photovoltaic panel.
  - Software prepared for communication with an external program written in any programming language.
  - Platform communication - serial (115200 b/s).

Functions:
  - R - calls the 'turnRight' function, which is responsible for moving the servo to the right by an angle in the range of 0 - 90,
  - L - calls the 'turnLeft' function, which is responsible for moving the servo to the left by an angle in the range of 0 - 90,
  - M - calls the 'measure' function, responsible for taking measurements with the INA219 sensor, presenting data on the measured quantities (voltage, current, power) and the current position of the servo.

*/


#include <Servo.h>
#include <Wire.h>
#include <Adafruit_INA219.h>

Adafruit_INA219 ina219;
Servo servoY;
Servo servoX;

 int posY = 90;
 int posX = 42;

void setup(){

servoY.attach(5);
servoX.attach(6);   
servoX.write(posX); 
servoY.write(posY); 

Serial.begin(115200);
  while (!Serial) {
      delay(1);
  }

  if (! ina219.begin()) {
    Serial.println("INA219 not found");
    while (1) { delay(10); }
  }
}

void loop(){
  
if (Serial.available()>0) {
 String command_move = Serial.readString();
  
 char cmd = command_move.charAt(0); 
 int deg=command_move.substring(1, 4).toInt();
 
switch (cmd){
  case 'R':
    turnRight(deg);
  break;

  case 'L' :
    turnLeft(deg);
  break;

  case 'M' :
   measure();
  break;
   }
 }
}
   
void turnRight(int deg){
    posY+=deg;
  servoY.write(posY);
}
  
void turnLeft(int deg){
    posY-=deg;
 servoY.write(posY);
} 

void measure(){
  
  float shuntvoltage = 0;
  float busvoltage = 0;
  float current_mA = 0;
  float loadvoltage = 0;
  float power_mW = 0;
  
  if (posY <= 180){
 Serial.print("Y position: ");
 Serial.println(posY);
 }
 else if (posY > 180){
 posY = 180;
 Serial.print("Max position: ");
 Serial.println(posY);
 }
 else if (posY < 0){
 posY = 0;
 Serial.print("Starting position: ");
 Serial.println(posY);
}
delay(500);

  shuntvoltage = ina219.getShuntVoltage_mV();
  busvoltage = ina219.getBusVoltage_V();
  current_mA = ina219.getCurrent_mA();
  power_mW = ina219.getPower_mW();
  loadvoltage = busvoltage + (shuntvoltage / 1000);
  delay(500);
  Serial.print("Load voltage:  "); Serial.print(loadvoltage); Serial.println(" V");
  Serial.print("Current:       "); Serial.print(current_mA); Serial.println(" mA");
  Serial.print("Power:         "); Serial.print(power_mW); Serial.println(" mW");
}