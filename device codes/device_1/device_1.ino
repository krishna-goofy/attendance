#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <IRrecv.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char* ssid = "Virus-Infected Wi-Fi";
const char* password = "meandmyhomiesmalhotra71124";
const char* serverUrl = "http://192.168.29.26:5000/attendance";

const uint16_t kIrLed = D1;  // IR transmitter pin
const int receivePin = D2;   // IR receiver pin

IRsend irsend(kIrLed);
IRrecv irrecv(receivePin);
decode_results results;

WiFiClient wifiClient;
HTTPClient http;

unsigned long lastCheckTime = 0;
unsigned long checkInterval = 5000;  // 5 seconds timeout for checking student presence
bool studentPresent = false;

void sendAttendanceData(String class_id, String student_name) {
  if (WiFi.status() == WL_CONNECTED) {
    http.begin(wifiClient, serverUrl);
    http.addHeader("Content-Type", "application/json");

    String requestData = "{\"class_id\": \"" + class_id + "\", \"student_name\": \"" + student_name + "\"}";
    int httpResponseCode = http.POST(requestData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.println("Error on sending POST: " + String(httpResponseCode));
    }
    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Setup started");  // Debugging statement
  irsend.begin();
  irrecv.enableIRIn();
  
  // Connect to WiFi
  Serial.println("Connecting to WiFi...");  // Debugging statement
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Continuously broadcast signal
  irsend.sendNEC(0xF7C03F, 32);  // Sample NEC code
  Serial.println("Broadcasting IR signal...");  // Check statement for broadcasting

  // Check for response signals
  if (irrecv.decode(&results)) {
    Serial.print("Received signal: 0x");
    Serial.println(results.value, HEX);  // Print received value in HEX format

    if (results.value == 0xE0E020DF) {  // Student validation response code
      Serial.println("Student validated and entered");
      sendAttendanceData("5", "krishna");  // Replace with actual class ID and student name
      studentPresent = true;  // Student is present
      lastCheckTime = millis();  // Reset check signal timer
    } else if (results.value == 0xE0E040BF) {  // Check signal code
      Serial.println("Check signal received");
      lastCheckTime = millis();  // Reset check signal timer
    }
    irrecv.resume(); // Receive the next value
  }

  // Check if the student with 0xE0E020DF code has left the classroom
  if (studentPresent && (millis() - lastCheckTime > checkInterval)) {
    Serial.println("Student with code 0xE0E020DF has left the classroom");
    studentPresent = false;  // Reset the student's presence status
  }

  delay(1000);  // Adjust delay as needed
}
