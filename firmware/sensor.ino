const int TRIG = 6;
const int ECHO = 3;
const long timeout = 30000;
const float V_sound = 0.0340;  // cm/uS at 15 deg C
const float Max_range = 30;
const float Error_code = 5000000.0;

// Sensor initialization
void sensorInit() {

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  // Set Trig low by default
  digitalWrite(TRIG, 0);
}
// Echo measure
long measureEcho(long timeout) {
  long delayTime_start = micros();
  while (digitalRead(ECHO) == LOW) {
    if ((micros() - delayTime_start) > timeout) {
      // This means that the echo has been Low longer than the timeout and it was'nt set to high even after the Trigger, Thus something must be wrong
      return -1;  //error code
    }
  }
  // executed only if there were no issues and the delay time was less than timeout
  long t1 = micros();
  while (digitalRead(ECHO) == HIGH) {
    if ((micros() - t1) > timeout) { // if this is executed this means object was out of range and 0 (No object is returned)
      return 0;
    }
  }
  long t2 = micros();
  return (t2 - t1); //current time - time just before echo was set to high
}

// get Distance
float getDistance() {
  float d;
  // Trigger pulse
  digitalWrite(TRIG, 0);
  delayMicroseconds(2);
  digitalWrite(TRIG, 1);
  delayMicroseconds(10);
  digitalWrite(TRIG, 0);

  // Echo detection
  long t = measureEcho(timeout);
  //distance calculated
  d = (V_sound * t) / 2;
  // returns either the distance if less than the max range or just 0 
  if (t!=-1 && d < Max_range){
    return d;
  }
  return 0;
}
