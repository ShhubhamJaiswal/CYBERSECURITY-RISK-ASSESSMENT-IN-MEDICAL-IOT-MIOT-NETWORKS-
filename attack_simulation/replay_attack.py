"""
replay_attack.py
Replays old signed packets to simulate a replay attack.
"""

from utils import sign, send, DEFAULT_DEVICE
import time

def run_replay(count=20):
    old_ts = int(time.time()) - 600  # 10 minutes old
    for i in range(count):
        ts = old_ts
        nonce = 2000 + i
        tempC, hr, spo2 = 36.5, 78, 97
        sig = sign(DEFAULT_DEVICE, ts, nonce, tempC, hr, spo2)

        payload = {
            "deviceId": DEFAULT_DEVICE,
            "ts": ts,
            "nonce": nonce,
            "tempC": tempC,
            "hr": hr,
            "spo2": spo2,
            "sig": sig,
        }

        code, text = send(payload, "replay")
        print(f"[{i}] {code} {text}")
        time.sleep(0.2)

if __name__ == "__main__":
    print("⚠️ Starting Replay Attack")
    run_replay(25)
    print("✅ Replay attack completed.")
