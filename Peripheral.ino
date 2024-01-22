#include <ArduinoBLE.h>

BLEService dataService("19B10000-E8F2-537E-4F6C-D104768A1214");
BLECharacteristic dataCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite, 20);

void setup() {
  Serial.begin(115200);

  while (!Serial);

  BLE.begin();
  

  BLE.setLocalName("BLE1");
  BLE.setAdvertisedService(dataService);
  dataService.addCharacteristic(dataCharacteristic);
  BLE.addService(dataService);
  

  BLE.advertise();

  Serial.println("BLE and UART Bidirectional Communication Peripheral");
}

void loop() {
    BLEDevice central = BLE.central();

    if (central) {
        Serial.print("Connected to central: ");
        Serial.println(central.address());

        while (central.connected()) {
            // Check for incoming data from central
            if (dataCharacteristic.written()) {
                const uint8_t* receivedData = dataCharacteristic.value();
                size_t length = dataCharacteristic.valueLength();  // Get the length of the data

                // Create a string with the correct length
                String receivedString = "";
                for (size_t i = 0; i < length; i++) {
                    receivedString += (char)receivedData[i];
                }

                Serial.print("Received from Central: ");
                Serial.println(receivedString);
            }
        }

        Serial.print("Disconnected from central: ");
        Serial.println(central.address());
    }
}
