#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);

  servo1.attach(9);
  servo2.attach(10);

  servo1.write(90);
  servo2.write(90);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    int comma = data.indexOf(',');

    if (comma > 0) {
      int angle1 = data.substring(0, comma).toInt();
      int angle2 = data.substring(comma + 1).toInt();

      angle1 = constrain(angle1, 0, 180);
      angle2 = constrain(angle2, 0, 180);

      servo1.write(angle1);
      servo2.write(angle2);
    }
  }
}
