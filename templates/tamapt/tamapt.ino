#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "LTT4G-36CD"; 
const char* password = "gTgLn95ibDM"; 

WebServer server(80);

// تعريف المخارج
const int rightPin = 32; // مخرج الانعطاف لليمين
const int leftPin = 33; // مخرج الانعطاف لليسار

void setup() {
    Serial.begin(115200);
    pinMode(rightPin, OUTPUT);
    pinMode(leftPin, OUTPUT);
    digitalWrite(rightPin, LOW);
    digitalWrite(leftPin, LOW);

    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // طباعة عنوان IP
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    server.on("/turn/right", []() {
        digitalWrite(rightPin, HIGH);
        delay(10000);
        digitalWrite(rightPin, LOW);
        server.send(200, "text/plain", "Right Turn Signal Activated");
    });

    server.on("/turn/left", []() {
        digitalWrite(leftPin, HIGH);
        delay(10000);
        digitalWrite(leftPin, LOW);
        server.send(200, "text/plain", "Left Turn Signal Activated");
    });

    server.begin();
}

void loop() {
    server.handleClient();
}
