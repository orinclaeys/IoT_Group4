#include <ArduinoBLE.h>

BLEService dataService("19B10000-E8F2-537E-4F6C-D104768A1214");
BLECharacteristic dataCharacteristic("19B10001-E8F2-537E-4F6C-D104768A1214", BLERead | BLEWrite, 20);

void setup() {
  Serial.begin(115200);
  while (!Serial);

  BLE.begin();
  Serial.println("Bluetooth® Low Energy Central - Bidirectional Communication");

  BLE.scanForUuid("19b10000-e8f2-537e-4f6c-d104768a1214");
}

void loop() {
  BLEDevice peripheral = BLE.available();

  if (peripheral) {
    Serial.print("Found ");
    Serial.print(peripheral.address());
    Serial.print(" '");
    Serial.print(peripheral.localName());
    Serial.print("' ");
    Serial.print(peripheral.advertisedServiceUuid());
    Serial.println();

    if (peripheral.localName() != "BLE1") {
      return;
    }

    BLE.stopScan();

    exchangeData(peripheral);

    BLE.scanForUuid("19b10000-e8f2-537e-4f6c-d104768a1214");
  }
}

void exchangeData(BLEDevice peripheral) {
  Serial.println("Connecting ...");

  if (peripheral.connect()) {
    Serial.println("Connected");
  } else {
    Serial.println("Failed to connect!");
    return;
  }

  Serial.println("Discovering attributes ...");
  if (peripheral.discoverAttributes()) {
    Serial.println("Attributes discovered");
  } else {
    Serial.println("Attribute discovery failed!");
    peripheral.disconnect();
    return;
  }

  BLECharacteristic dataCharacteristic = peripheral.characteristic("19b10001-e8f2-537e-4f6c-d104768a1214");

  if (!dataCharacteristic) {
    Serial.println("Peripheral does not have data characteristic!");
    peripheral.disconnect();
    return;
  }

  while (peripheral.connected()) {
    // Check for incoming data from peripheral
    if (dataCharacteristic.written()) {
      const uint8_t* receivedData = dataCharacteristic.value();
      Serial.print("Received from Peripheral: ");
      Serial.println(reinterpret_cast<const char*>(receivedData));
    }

    // Read from UART and send to peripheral via BLE
    if (Serial.available()) {
      String message = Serial.readString();
      Serial.print("Sent to Peripheral: ");
      Serial.println(message);
      dataCharacteristic.writeValue(message.c_str(), message.length());
    }
  }

  Serial.println("Peripheral disconnected");
}
