
void setup() {
  Serial.begin(9600);
  sensorInit();
  servoInit();
}
void sweep() {
  float D;  // distance variable being declared locally
  //Positive Sweep
  for (int i = 15; i <= 165; i += 1) {
    moveTo(i);
    delay(10);
    D = getDistance();
    Serial.print(i);  // Angle
    Serial.print(",");
    Serial.println(D);  // Distance
    delay(20);
  }
  //Negative sweep
  for (int i = 165; i >= 15; i -= 1) {
    moveTo(i);
    delay(10);
    D = getDistance();
    Serial.print(i);  // Angle
    Serial.print(",");
    Serial.println(D);  // Distance
    delay(20);
  }
}

void loop() {
  sweep();
}
