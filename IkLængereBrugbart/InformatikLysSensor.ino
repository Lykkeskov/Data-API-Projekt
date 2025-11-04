//Brug WEMOS D1 MINI ESP32
// Definer pins der bruges
const int lysSensorPin1 = 34;
const int buttonPin = 19;
const int ledPin = 18;

const int delayTime = 1000;
unsigned long previousMillis = 0;

bool ledState = LOW;

void setup() {
  // Sæt sensorer til at være inputs
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);

  digitalWrite(ledPin, ledState);

  Serial.begin(9600);
}

void loop() {
  int buttonState = digitalRead(buttonPin);
  unsigned long currentMillis = millis();
  
  if (buttonState == LOW && currentMillis - previousMillis >= delayTime) {
    previousMillis = currentMillis;
    
    Serial.print("Sensor 1:");
    Serial.println(analogRead(lysSensorPin1));
    
    ledState = !ledState;
    digitalWrite(ledPin, ledState);
  }


}
