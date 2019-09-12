#include <MPU9250_asukiaaa.h>
MPU9250_asukiaaa mySensor;
float aX, aY, aZ, aSqrt;
float gX, gY, gZ;

void setup() {
  Wire.begin();
  Serial.begin(115200);
  mySensor.setWire(&Wire);
  mySensor.beginAccel();
  mySensor.beginGyro();
}

void loop()
{
    static uint32_t prev_ms = millis();
    if ((millis() - prev_ms) > 100)
    {
      mySensor.accelUpdate();
      aX = mySensor.accelX();
      aY = mySensor.accelY();
      aZ = mySensor.accelZ();
      aSqrt = mySensor.accelSqrt();
      Serial.print(aX);
      Serial.print("\t");
      Serial.print(aY);
      Serial.print("\t");
      Serial.print(aZ);
//      Serial.print("\t");
     
//      mySensor.gyroUpdate();
//      gX = mySensor.gyroX();
//      gY = mySensor.gyroY();
//      gZ = mySensor.gyroZ();
//      Serial.print(gX);
//      Serial.print("\t");
//      Serial.print(gY);
//      Serial.print("\t");
//      Serial.print(gZ);
      Serial.println();
      
      prev_ms = millis();
  }
}
