import argparse
import json
import socket
import statistics
import time


def message(msg_id):
    return {
        "version": "1.0",
        "id": str(msg_id),
        "type": "system",
        "action": "ping",
        "data": {},
    }


def main():
    parser = argparse.ArgumentParser(description="Measure SmartDesk TCP ping latency")
    parser.add_argument("host")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--token", required=True)
    parser.add_argument("--count", type=int, default=20)
    args = parser.parse_args()

    samples = []
    failures = 0
    sock = socket.create_connection((args.host, args.port), timeout=5)
    sock.settimeout(3)
    file = sock.makefile("rwb")

    try:
        file.readline()
        resume = {"version": "1.0", "id": "0", "type": "auth", "action": "resume", "data": {"token": args.token}}
        file.write((json.dumps(resume) + "\n").encode())
        file.flush()
        response = json.loads(file.readline().decode())
        if response.get("status") != "ok":
            raise RuntimeError("Session resume failed")

        for i in range(1, args.count + 1):
            msg = message(i)
            msg["token"] = args.token
            started = time.perf_counter()
            file.write((json.dumps(msg) + "\n").encode())
            file.flush()
            line = file.readline()
            if not line:
                failures += 1
                continue
            response = json.loads(line.decode())
            if response.get("status") == "ok":
                samples.append((time.perf_counter() - started) * 1000)
            else:
                failures += 1
    finally:
        file.close()
        sock.close()

    total = args.count
    success_rate = len(samples) / total * 100 if total else 0
    print(f"Samples: {total}")
    print(f"Successful: {len(samples)}")
    print(f"Failed: {failures}")
    print(f"Success rate: {success_rate:.2f}%")
    if samples:
        print(f"Average RTT: {statistics.mean(samples):.2f} ms")
        print(f"Minimum RTT: {min(samples):.2f} ms")
        print(f"Maximum RTT: {max(samples):.2f} ms")


if __name__ == "__main__":
    main()
