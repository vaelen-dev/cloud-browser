import sys
import socket
import json
import base64

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

    # Read 4-byte length prefix
    raw_len = s.recv(4)
    if not raw_len:
        print(json.dumps({"error": "Empty response"}))
        return
    total_len = int.from_bytes(raw_len, "big")

    data = b""
    while len(data) < total_len:
        chunk = s.recv(min(65536, total_len - len(data)))
        if not chunk:
            break
        data += chunk
    s.close()

    res = json.loads(data.decode())
    b64 = res.pop("screenshot_b64", None)
    if b64:
        with open("/tmp/live_ss.png", "wb") as f:
            f.write(base64.b64decode(b64))
        res["screenshot"] = "/tmp/live_ss.png"

    print(json.dumps(res))

if __name__ == "__main__":
    main()
