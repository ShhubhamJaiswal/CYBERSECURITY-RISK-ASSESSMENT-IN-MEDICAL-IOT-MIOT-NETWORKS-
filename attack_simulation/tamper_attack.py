"""
tamper_attack.py
Sends packets with valid signatures but tampered values.
"""

from utils import sign, send, DEFAULT_DEVICE
import time, random

def run_tamper(count=20):
    for i in range(count):
        ts = int(time.time())
        nonce = 1000 + i
        tempC, hr, spo2 = 36.6, 75, 98

        sig = sign(DEFAULT_DEVICE, ts, nonce, tempC, hr, spo2)

        # tamper HR drastically
        tampered_hr = random.choice([200, 5, 300])

        payload = {
            "deviceId": DEFAULT_DEVICE,
            "ts": ts,
            "nonce": nonce,
            "tempC": tempC,
            "hr": tampered_hr,
            "spo2": spo2,
            "sig": sig,
        }

        code, text = send(payload, "tamper")
        print(f"[{i}] {code} {text}")

if __name__ == "__main__":
    print("⚠️ Starting Tamper Attack")
    run_tamper(30)
    print("✅ Tamper attack completed.")
