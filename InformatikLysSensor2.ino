#include <WiFi.h>
#include <HTTPClient.h>

const int lysSensorPin1 = 34;
const int buttonPin = 19;
const int ledPin = 18;
 
const int delayTime = 1000;
unsigned long previousMillis = 0;

bool ledState = LOW;

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";
const char* server = "http://yourusername.pythonanywhere.com/data";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("Connected to WiFi");

  // Sæt sensorer til at være inputs
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);

}

void loop() {
  int buttonState = digitalRead(buttonPin);
  unsigned long currentMillis = millis();

  if (buttonState == LOW && currentMillis - previousMillis >= delayTime) {
    previousMillis = currentMillis;    

    ledState = !ledState;
    digitalWrite(ledPin, ledState);

    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;
      http.begin(server);
      http.addHeader("Content-Type", "application/json");

      String json = "{\"temperature\":25.5, \"humidity\":60}";
      int httpResponseCode = http.POST(json);

      Serial.print("Response: ");
      Serial.println(httpResponseCode);

      http.end();
    }
    delay(5000);
  }
}
