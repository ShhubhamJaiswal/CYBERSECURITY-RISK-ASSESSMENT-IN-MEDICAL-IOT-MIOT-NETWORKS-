# 🩺 MIoT-Secure: Cyber-Resilient Medical IoT Remote Patient Monitoring System

## 📌 Project Overview
**MIoT-Secure** is an end-to-end Medical Internet of Things (MIoT) ecosystem designed for secure remote patient monitoring. It defends continuous medical data streams against common cybersecurity attack vectors using edge cryptography, secure serverless cloud ingestion, and unsupervised machine learning.

The system captures patient vitals (precision body temperature, pulse rate, oxygen levels, and atmospheric conditions) via an ESP32 hardware node, signs and transmits them securely, and monitors the telemetry on an interactive threat intelligence dashboard.

```
       +-----------------------+
       |   ESP32 Edge Node     | (DS18B20 Temp, BMP180 Temp/Press/Alt, MAX30102 HR/SpO2)
       +-----------+-----------+
                   |
                   | Secure JSON payload with HMAC-SHA256
                   v
       +-----------------------+
       |   Firebase Functions  | (Cryptographic Handshake, Nonce Tracking, Skew Checks)
       +-----------+-----------+
                   |
                   | Authorized Readings & Security Alerts
                   v
       +-----------------------+
       | Firebase Realtime DB  |
       +-----------+-----------+
                   |
                   v
       +-----------------------+
       | Streamlit Dashboard   | (Real-time Monitoring, Outlier Scans, Analytics)
       +-----------+-----------+
                   |
                   +---> [Isolation Forest ML Model] (Unsupervised Anomaly Detector)
```

---

## 🚀 Key Features

### 📡 1. Embedded Sensing (Edge Layer)
* **ESP32 Edge Microcontroller:** Serves as the primary medical telemetry platform.
* **Precision Sensor Integration:**
  * **DS18B20:** High-precision digital thermometer operating via the OneWire bus.
  * **BMP180:** Barometric pressure and temperature sensor.
  * **MAX30102 / MAX30105:** Photoplethysmogram (PPG) pulse oximetry sensor measuring heart rate (bpm) and blood oxygen saturation ($SpO_2$ %).
* **Cryptographic Edge Signing:** Computes dynamic HMAC-SHA256 signatures for every reading using a pre-shared hardware secret, ensuring message integrity and non-repudiation.

### 🛡️ 2. Secure Cloud Ingestion (Transit & Cloud Layer)
* **Firebase Cloud Functions (Node.js 18 + Express):** Serve as the secure ingestion gatekeeper (`/ingestReading`).
* **Cryptographic Signature Verification:** Validates that incoming telemetry packets originate from an authorized device using a shared key.
* **Timestamp Skew Prevention:** Blocks delayed packet submission (replay attacks or stale data) by enforcing a strict time window of $\pm 120$ seconds.
* **Stateful Nonce Protection:** Registers nonces to detect and discard duplicate or replayed packets.
* **Rule-Based Emergency Triggers:** Performs rapid out-of-range safety verification (e.g., heart rate $< 40$ or $> 160$ bpm, body temperature $< 35^\circ\text{C}$ or $> 39^\circ\text{C}$) to flag medical emergencies instantly.

### 📊 3. Interactive Threat Intelligence Dashboard (Analytics Layer)
* **Streamlit Real-Time Dashboard:** A unified workspace for clinicians and cybersecurity analysts.
* **Live Dynamic Stream:** Automatically polls authorized biometric histories from Firebase and visualizes them through high-fidelity gauges, time-series line charts, and metric panels.
* **Correlation Analytics:** Explores multi-variable parameters using Plotly scatter matrices.
* **Live Security Incident Feed:** Displays critical security violations logged in Firebase (e.g., signature failures, replay attacks, timestamp discrepancies, and rule-based medical thresholds).

### 🧠 4. Machine Learning Anomaly Detection (Defensive Shield)
* **Unsupervised Isolation Forest Classifier:** Continuously scans multidimensional telemetry matrices (Heart Rate, $SpO_2$, DS18B20 Temp, BMP180 Temp, BMP180 Pressure) to identify stealthy parameters tampering.
* **Synthetic Bootstrapping:** In the absence of live physical sensor history, the training engine dynamically generates mathematical normal distribution profiles of human vitals for secure model calibration.
* **One-Click Retraining:** Enables on-the-fly model re-tuning directly from the sidebar controls.

### 💥 5. Adversarial Attack Simulation (Offensive Security)
* **Offensive Script Suite:** Python utilities to simulate authentic attacker profiles:
  * `tamper_attack.py`: Injects medically dangerous parameters (e.g., heart rates of 300 bpm or 5 bpm) inside packets with valid cryptographic signatures.
  * `replay_attack.py`: Replays historic valid messages with stale timestamps to test time-skew filters.
  * `spoofing_attack.py`: Forges fake device IDs and corrupts signature blocks to evaluate ingestion authorization.
  * `dos_attack.py`: Launches multi-threaded socket-flooding storms to simulate volumetric denial-of-service conditions.
* **Auditing Logs:** Records latency, HTTP status codes, and payload receipts in CSV formats under `attack_simulation/attack_logs/` for security telemetry correlation.

---

## 📂 Project Directory Structure

```
miot-secure-project/
├── device/
│   └── config/
│       └── config.h            # Hardware pin configurations, Wi-Fi keys, HMAC secret
├── src/
│   └── main.cpp                # ESP32 Arduino firmware (sensors, networking, Firebase push)
├── cloud_functions/
│   └── functions/
│       ├── index.js            # Node.js serverless app (HMAC validation, replay & skew checks)
│       ├── package.json        # Node.js dependencies
│       └── .env                # Serverless credentials
├── streamlit_dashboard/
│   ├── app.py                  # Interactive Streamlit Web App
│   ├── isolation_forest_model.py # ML model training pipeline (Isolation Forest)
│   ├── isolation_model.joblib  # Serialized model binary
│   ├── serviceAccountKey.json  # Firebase SDK connection credentials
│   └── requirements.txt        # Dashboard dependencies
├── attack_simulation/
│   ├── utils.py                # Payload signers, POST handlers, CSV audit reporters
│   ├── tamper_attack.py        # Valid-signature metric manipulation
│   ├── replay_attack.py        # Stale timestamp payload injection
│   ├── spoofing_attack.py      # Rogue device spoofing and signature corruption
│   ├── dos_attack.py           # Multi-threaded socket-level stress simulation
│   ├── requirements.txt        # Attack tool dependencies
│   └── attack_logs/            # Audit records of attack simulations (CSV)
├── tests/
│   ├── test_anomaly_detection.py # unittest suite for model verification
│   └── data/                   # Mock verification files
├── platformio.ini              # PlatformIO project configuration for ESP32
├── requirements.txt            # Root global virtual environment requirements
└── README.md                   # Project documentation
```

---

## 🛠️ Installation & Setup Guide

### 📋 Prerequisites
Ensure the following are installed:
* **Python 3.11+**
* **Node.js v18+ & npm**
* **PlatformIO CLI / VS Code IDE**
* **Firebase Account & Firebase CLI** (`npm install -g firebase-tools`)

---

### Step 1: Firebase & Cloud Functions Deployment

1. **Create a Firebase Project:**
   * Go to the [Firebase Console](https://console.firebase.google.com/) and create a project named `miot-project` (or similar).
   * Enable **Realtime Database** (choose US Central or your preferred region).
   * Enable **Cloud Functions** (requires the Pay-As-You-Go Blaze plan, which offers a generous free tier).

2. **Configure Cloud Functions Locally:**
   * Log into Firebase using the CLI:
     ```bash
     firebase login
     ```
   * Link your local repository to your Firebase project:
     ```bash
     firebase use --add
     ```
   * Define the pre-shared secret in Firebase runtime configuration (must match the device config):
     ```bash
     firebase functions:config:set hmac.secret="k9zP!7qR$*sXvL2wF@mJbH3nTgA"
     ```

3. **Deploy the Cloud Function:**
   * Navigate to the cloud functions directory:
     ```bash
     cd cloud_functions/functions
     npm install
     ```
   * Deploy the function to Google Cloud:
     ```bash
     firebase deploy --only functions
     ```
   * Save the generated endpoint URL (it will look like `https://<region>-<project-id>.cloudfunctions.net/ingestReading`).

---

### Step 2: Streamlit Dashboard Configuration

1. **Generate Firebase Service Account Credentials:**
   * In the Firebase Console, go to **Project Settings > Service Accounts**.
   * Click **Generate New Private Key**, download the JSON file, and save it as:
     `streamlit_dashboard/serviceAccountKey.json`

2. **Set up Python Virtual Environment:**
   * Return to the project root and create a virtual environment:
     ```bash
     python -m venv .venv
     # Windows:
     .venv\Scripts\activate
     # macOS/Linux:
     source .venv/bin/activate
     ```
   * Install dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Train the Anomaly Detection Model:**
   * Run the model training script. It fetches historical data from Firebase (or falls back to a synthetic dataset) and saves the trained Isolation Forest model:
     ```bash
     python streamlit_dashboard/isolation_forest_model.py
     ```

4. **Run the Interactive Dashboard:**
   * Run the Streamlit application:
     ```bash
     streamlit run streamlit_dashboard/app.py
     ```
   * Open the dashboard in your browser (usually at `http://localhost:8501`).

---

### Step 3: ESP32 Hardware Firmware Setup

1. **Configure Hardware Variables:**
   * Open `device/config/config.h` and update with your network configuration and Cloud Function URL:
     ```cpp
     #define WIFI_SSID "Your_WiFi_Name"
     #define WIFI_PASS "Your_WiFi_Password"
     #define CLOUD_FN_URL "https://<region>-<project-id>.cloudfunctions.net/ingestReading"
     #define HMAC_SECRET "k9zP!7qR$*sXvL2wF@mJbH3nTgA" // Must match Step 1
     ```

2. **Compile and Flash Firmware:**
   * Connect your ESP32 board to your computer via USB.
   * Run PlatformIO compilation and upload commands:
     ```bash
     pio run --target upload
     ```
   * Open the Serial Monitor at `115200` baud rate to verify connections and view real-time transmissions:
     ```bash
     pio device monitor
     ```

---

## 🔒 Security Posture Analysis

### 🛡️ Defensive Mechanics in Action

The serverless gatekeeper verifies several key properties of each message before storing it in the database:

1. **HMAC Integrity & Authentication Handshake:**
   The ESP32 constructs a canonical message string:
   $$\text{canonical} = \text{deviceId} \parallel "|" \parallel \text{ts} \parallel "|" \parallel \text{nonce} \parallel "|" \parallel \text{tempC} \parallel "|" \parallel \text{hr} \parallel "|" \parallel \text{spo2}$$
   Using the `HMAC-SHA256` hashing algorithm with the pre-shared key, it generates a unique cryptographic signature. Any alteration to the data mid-transit (e.g., parameter tampering) results in signature mismatches, which are flagged and blocked immediately.

2. **Replay Attack Defensive Verification:**
   Rogue actors capturing a valid transmission cannot resend it to skew patient histories because:
   * **Time-Freshness Gate:** The function compares the incoming timestamp (`ts`) with the server clock (`now`). If $|now - ts| > 120\text{ seconds}$, the message is rejected.
   * **Stateful Nonce Registry:** Nonces are unique identifiers. If a nonce has already been registered, the message is rejected.

---

## 🧪 Simulation & Automated Verification

### Running Cybersecurity Attacks
Validate the resilience of the system by launching adversarial payloads from the `attack_simulation/` directory:

* **Simulate Parameter Tampering:**
  Sends payload signed with the correct cryptographic key, but containing spoofed, medically extreme readings.
  ```bash
  python attack_simulation/tamper_attack.py
  ```
* **Simulate Packet Replaying:**
  Intercepts or duplicates old messages with stale timestamps to test the time-freshness validation of the ingestion gateway.
  ```bash
  python attack_simulation/replay_attack.py
  ```
* **Simulate Node Spoofing:**
  Simulates rogue hardware nodes attempting to inject forged metrics under invalid device profiles.
  ```bash
  python attack_simulation/spoofing_attack.py
  ```
* **Simulate Denial of Service (DoS):**
  Spams TCP connections to a target IP/port to assess the node's resistance against resource exhaustion.
  ```bash
  python attack_simulation/dos_attack.py
  ```

---

### Running Unit Tests
You can run the regression tests using Python's built-in `unittest` framework to verify that the model pipeline and Firebase connectors are operating correctly:

```bash
python -m unittest tests/test_anomaly_detection.py
```

---

## 🛠️ Technologies & Libraries

* **Microcontroller Firmware:** Arduino, PlatformIO, ESP32, Firebase ESP32 Client, DallasTemperature, SparkFun MAX3010x.
* **Backend & Cloud:** Firebase Cloud Functions, Node.js, Express.js, Crypto, CORS, Firebase Realtime Database.
* **Visual Analytics & AI:** Python 3.11, Streamlit, Scikit-Learn (Isolation Forest), Pandas, NumPy, Plotly Express, Joblib.
* **Offensive Simulation:** Python Requests, HMAC, Hashlib, Multi-threading, CSV Logging.
