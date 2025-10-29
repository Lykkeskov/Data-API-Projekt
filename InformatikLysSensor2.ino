#include <WiFi.h>
#include <HTTPClient.h>

// --- Pins ---
const int buttonPin = 19;
const int ledPin = 18;

// --- Timing ---
const int delayTime = 3000;
unsigned long previousMillis = 0;
bool ledState = LOW;

// --- WiFi ---
const char* ssid = "Tobias_iPhone";
const char* password = "iPhoneNet";
const char* server = "http://halfdan.pythonanywhere.com/data";

void setup() {
  Serial.begin(115200);
  
  // Setup pins
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(ledPin, OUTPUT);

  // Connect to WiFi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nConnected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  int buttonState = digitalRead(buttonPin);
  unsigned long currentMillis = millis();

  // Trigger when button pressed and delay time passed
  if (buttonState == LOW && currentMillis - previousMillis >= delayTime) {
    previousMillis = currentMillis;

    // Toggle LED
    ledState = !ledState;
    digitalWrite(ledPin, ledState);

    // Read light level
    int lysniveau = analogRead(34);
    int lokale = 211;

    sendData(lokale, lysniveau);
  }
}

void sendData(int lokale, int lysniveau) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(server);
    http.addHeader("Content-Type", "application/json");

    // Build JSON payload
    String json = "{\"lokale\":";
    json += lokale;
    json += ",\"lysniveau\":";
    json += lysniveau;
    json += "}";

    Serial.print("Sending data: ");
    Serial.println(json);

    int httpResponseCode = http.POST(json);

    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Server response: ");
      Serial.println(response);
    } else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi not connected. Reconnecting...");
    WiFi.reconnect();
  }
}
