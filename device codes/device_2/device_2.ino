#include <IRremoteInt.h>
#include <IRremote.h>

int RECV_PIN = 11; //define input pin on Arduino
IRrecv irrecv(RECV_PIN);
decode_results results;
void setup() {
  Serial.begin(9600);
  irrecv.enableIRIn(); // Start the receiver

}
void loop() {
  if (irrecv.decode( & results)) {
    String hex = String(results.value, HEX);
    Serial.print("Hexadecimal Code: ");
    Serial.println(hex);
    irrecv.resume(); // Receive the next value
  }
}
