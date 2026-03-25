
byte servo_pin = 11;

#include <Servo.h>
Servo myservo;

void servoInit() {
  myservo.attach(servo_pin);
  myservo.write(90);
}

void moveTo(int angle){
  myservo.write(angle);
}


