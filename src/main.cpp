#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include "MAX30105.h"
#include <time.h>

// ---------- WiFi ----------
#define WIFI_SSID "Galaxy M34 5G 8FCF"
#define WIFI_PASSWORD "12345678"

// ---------- Firebase ----------
const char* FIREBASE_URL = "https://miot--project-9560d-default-rtdb.firebaseio.com";

// ---------- DS18B20 ----------
const int oneWireBus = 4;
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);

// ---------- BMP180 ----------
Adafruit_BMP085 bmp;

// ---------- MAX30102 ----------
MAX30105 particleSensor;

// ---------- Sensor Data ----------
float ds18b20Temp;
float bmpTemp, bmpPressure, bmpAltitude;
float heartRate, spo2;

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("🚀 Booting MIoT Healthcare Device...");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi Connected!");
  Serial.println(WiFi.localIP());

  configTime(0, 0, "pool.ntp.org");

  sensors.begin();

  if (!bmp.begin()) {
    Serial.println("❌ BMP180 not found!");
    while (1);
  }

  if (!particleSensor.begin(Wire, I2C_SPEED_STANDARD)) {
    Serial.println("❌ MAX30102 not found!");
    while (1);
  }
  particleSensor.setup();
  particleSensor.setPulseAmplitudeRed(0x0A);
  particleSensor.setPulseAmplitudeGreen(0);
  Serial.println("✅ Sensors Ready!");
}

void loop() {
  Serial.println("--------------------------------------------");
  Serial.println("📡 Reading sensor data...");

  sensors.requestTemperatures();
  ds18b20Temp = sensors.getTempCByIndex(0);

  bmpTemp = bmp.readTemperature();
  bmpPressure = bmp.readPressure();
  bmpAltitude = bmp.readAltitude();

  long irValue = particleSensor.getIR();
  if (irValue > 50000) {
    heartRate = random(70, 100); // Placeholder
    spo2 = random(95, 100);      // Placeholder
  } else {
    heartRate = 0;
    spo2 = 0;
  }

  Serial.printf("🌡 DS18B20: %.2f °C\n", ds18b20Temp);
  Serial.printf("🌤 BMP180: %.2f °C | %.2f Pa | %.2f m\n", bmpTemp, bmpPressure, bmpAltitude);
  Serial.printf("❤️ HeartRate: %.2f bpm | 🩸 SpO2: %.2f %%\n", heartRate, spo2);

  String json = "{";
  json += "\"BMP180_Temp\":" + String(bmpTemp, 2) + ",";
  json += "\"BMP180_Pressure\":" + String(bmpPressure, 0) + ","; // Send as integer
  json += "\"BMP180_Altitude\":" + String(bmpAltitude, 2) + ",";
  json += "\"DS18B20_Temp\":" + String(ds18b20Temp, 2) + ",";
  json += "\"HeartRate\":" + String(heartRate, 0) + ","; // Send as integer
  json += "\"SpO2\":" + String(spo2, 0) + ",";           // Send as integer
  
  json += "\"ts\":" + String(time(nullptr));
  
  json += "}"; 
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    
    String url = String(FIREBASE_URL) + "/readings/esp32-01.json";
    
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    
    Serial.printf("Sending POST to: %s\n", url.c_str());
    
    int code = http.POST(json); 
    
    if (code > 0) {
      Serial.printf("✅ Data pushed to Firebase | Code: %d\n", code);
    } else {
      Serial.printf("❌ Firebase Error: %s\n", http.errorToString(code).c_str());
    }
    http.end();
  }

  delay(5000); 
}