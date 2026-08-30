#ifndef CONFIG_H
#define CONFIG_H

// ==== WiFi Config ====
// Replace with your network details
#define WIFI_SSID "AirFiber-ohR4ju" // YOUR ACTUAL SSID
#define WIFI_PASS "dosee9yenge0Jie0" // YOUR ACTUAL PASSWORD

// ==== Cloud Function Endpoint ====
// Replace YOUR_PROJECT with your actual Firebase Project ID
#define CLOUD_FN_URL "https://us-central1-miot--project-9560d.cloudfunctions.net/ingestReading"

// ==== Device Identity ====
// You can keep this or change it
#define DEVICE_ID "esp32-01"

// ==== Security Secret (HMAC) ====
// IMPORTANT: Replace with a strong, random secret key
// This MUST exactly match the environment variable set in your Cloud Function
#define HMAC_SECRET "k9zP!7qR$*sXvL2wF@mJbH3nTgA" // YOUR ACTUAL SECRET KEY

// ==== DS18B20 Pin ====
// Define the GPIO pin connected to the DS18B20 data line
#define ONE_WIRE_BUS 4  // <--- MAKE SURE THIS LINE EXISTS AND IS UNCOMMENTED

// ==== Data Sending Interval (ms) ====
// How often to send data (5000ms = 5 seconds)
#define SEND_INTERVAL 5000

#endif // CONFIG_H

