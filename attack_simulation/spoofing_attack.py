"""
spoofing_attack.py
Sends packets from fake device IDs with invalid signatures.
"""

from utils import send
import time, random

def run_spoof(count=20):
    for i in range(count):
        deviceId = f"esp32-fake{random.randint(100,999)}"
        ts = int(time.time())
        nonce = 3000 + i
        tempC, hr, spo2 = 40.0, 45, 70
        sig = "deadbeef" * 8  # invalid

        payload = {
            "deviceId": deviceId,
            "ts": ts,
            "nonce": nonce,
            "tempC": tempC,
            "hr": hr,
            "spo2": spo2,
            "sig": sig,
        }

        code, text = send(payload, "spoofing")
        print(f"[{i}] {code} {text}")

if __name__ == "__main__":
    print("⚠️ Starting Spoofing Attack")
    run_spoof(30)
    print("✅ Spoofing attack completed.")
