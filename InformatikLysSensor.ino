// Pins for lys sensor 1 og 2
const int  LysSensorPin1 = 34;

void setup() {
  // Sæt sensorer til at være inputs


  Serial.begin(9600);
}

void loop() {
  Serial.print("Sensor 1:");
  Serial.println(analogRead(LysSensorPin1));

delay(50);

}
