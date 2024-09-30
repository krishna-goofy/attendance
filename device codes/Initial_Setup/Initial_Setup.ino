#include <Adafruit_Fingerprint.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(4, 5); // RX, TX
Adafruit_Fingerprint finger = Adafruit_Fingerprint(&mySerial);

void setup() {
  Serial.begin(9600);
  mySerial.begin(57600);
  
  if (finger.verifyPassword()) {
    Serial.println("Fingerprint sensor detected.");
  } else {
    Serial.println("Fingerprint sensor not detected.");
    while (1);
  }

  Serial.println("Please place your finger on the sensor to enroll.");
}

void loop() {
  Serial.println("Waiting for valid finger to enroll...");
  int id = getFingerprintEnroll();
  if (id > 0) {
    Serial.print("Enrolled successfully with ID "); Serial.println(id);
  }
  delay(5000);  // Wait before the next enrollment
}

// Function to enroll fingerprint
int getFingerprintEnroll() {
  int p = -1;
  Serial.print("Enter ID # for this fingerprint: ");
  while (p == -1) {
    p = Serial.parseInt();  // Read ID from serial monitor
  }
  
  Serial.print("Enrolling ID #");
  Serial.println(p);
  
  while (!getFingerprintEnrollHelper(p)) { 
    // Keep trying until enrollment succeeds
  }
  return p;
}

boolean getFingerprintEnrollHelper(int id) {
  int p = -1;
  Serial.print("Waiting for valid finger to enroll as ID #"); Serial.println(id);
  
  // Wait for a finger to be placed on the sensor
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    switch (p) {
      case FINGERPRINT_OK:
        Serial.println("Image taken");
        break;
      case FINGERPRINT_NOFINGER:
        Serial.println("No finger detected");
        break;
      case FINGERPRINT_PACKETRECIEVEERR:
        Serial.println("Communication error");
        break;
      case FINGERPRINT_IMAGEFAIL:
        Serial.println("Imaging error");
        return false;
      default:
        Serial.println("Unknown error");
        return false;
    }
  }

  // Convert the image to a fingerprint template
  p = finger.image2Tz(1);
  switch (p) {
    case FINGERPRINT_OK:
      Serial.println("Image converted");
      break;
    case FINGERPRINT_IMAGEMESS:
      Serial.println("Image too messy");
      return false;
    case FINGERPRINT_PACKETRECIEVEERR:
      Serial.println("Communication error");
      return false;
    case FINGERPRINT_FEATUREFAIL:
      Serial.println("Could not find fingerprint features");
      return false;
    case FINGERPRINT_INVALIDIMAGE:
      Serial.println("Invalid image");
      return false;
    default:
      Serial.println("Unknown error");
      return false;
  }

  Serial.println("Remove your finger");
  delay(2000);

  p = -1;
  Serial.println("Place the same finger again");
  while (p != FINGERPRINT_OK) {
    p = finger.getImage();
    if (p != FINGERPRINT_OK) return false;
  }

  p = finger.image2Tz(2);
  if (p != FINGERPRINT_OK) return false;

  // Create the model
  p = finger.createModel();
  if (p != FINGERPRINT_OK) return false;

  // Store the model with the given ID
  p = finger.storeModel(id);
  if (p == FINGERPRINT_OK) {
    Serial.println("Fingerprint enrolled successfully");
    return true;
  } else {
    Serial.println("Error enrolling fingerprint");
    return false;
  }
}
