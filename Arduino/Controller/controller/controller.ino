#include <SoftwareSerial.h>
#include <Firmata.h>

SoftwareSerial btSerial(10, 9);

void setup() {
  // put your setup code here, to run once:
  Firmata.setFirmwareVersion(0, 1);
  Firmata.begin(btSerial);


}

void loop() {
  // put your main code here, to run repeatedly:
  while (btSerial.available()) {
    Firmata.processInput();
  }

}
