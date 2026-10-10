import sys
import socket
import json

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No action"}))
        return

    action = sys.argv[1]
    args = sys.argv[2:]

    payload = json.dumps({"action": action, "args": args}).encode()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 9000))
    s.sendall(payload)

    data = b""
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
    s.close()
    print(data.decode())

if __name__ == "__main__":
    main()
