import json
import queue
import socket
import threading
import time
import tkinter as tk
from tkinter import messagebox

DISCOVERY_PORT = 8766
PROTOCOL_VERSION = "1.0"


class SmartDeskClient:
    def __init__(self, root):
        self.root = root
        self.sock = None
        self.reader_thread = None
        self.running = False
        self.token = None
        self.host = None
        self.responses = queue.Queue()
        self.next_id = 1

        root.title("SmartDesk Test Client")
        root.geometry("760x650")

        top = tk.Frame(root)
        top.pack(fill="x", padx=10, pady=8)
        tk.Button(top, text="Discover", command=self.discover).pack(side="left")
        tk.Button(top, text="Connect", command=self.connect).pack(side="left", padx=5)
        tk.Button(top, text="Disconnect", command=self.disconnect).pack(side="left")
        self.status = tk.Label(top, text="Disconnected")
        self.status.pack(side="left", padx=15)

        pair = tk.Frame(root)
        pair.pack(fill="x", padx=10)
        tk.Label(pair, text="Host IP:").pack(side="left")
        self.ip = tk.Entry(pair, width=16)
        self.ip.insert(0, "127.0.0.1")
        self.ip.pack(side="left", padx=4)
        tk.Label(pair, text="Port:").pack(side="left")
        self.port = tk.Entry(pair, width=7)
        self.port.insert(0, "8765")
        self.port.pack(side="left", padx=4)
        tk.Label(pair, text="Pair code:").pack(side="left")
        self.code = tk.Entry(pair, width=9)
        self.code.pack(side="left", padx=4)
        tk.Button(pair, text="Pair", command=self.pair).pack(side="left")

        info = tk.LabelFrame(root, text="Host information")
        info.pack(fill="x", padx=10, pady=8)
        self.info = tk.Label(info, text="No host information", anchor="w", justify="left")
        self.info.pack(fill="x", padx=8, pady=6)

        pad = tk.LabelFrame(root, text="Touchpad")
        pad.pack(fill="x", padx=10, pady=5)
        self.touch = tk.Canvas(pad, height=180, bg="white", highlightthickness=1)
        self.touch.pack(fill="x", padx=8, pady=8)
        self.touch.bind("<Motion>", self.mouse_move)
        self.touch.bind("<Button-1>", lambda e: self.send("mouse", "left_click"))
        self.touch.bind("<Button-3>", lambda e: self.send("mouse", "right_click"))
        self.touch.bind("<Double-Button-1>", lambda e: self.send("mouse", "double_click"))
        self.touch.bind("<MouseWheel>", self.mouse_scroll)

        buttons = tk.Frame(root)
        buttons.pack(fill="x", padx=10, pady=5)
        for label, action in [("Play/Pause", "play_pause"), ("Next", "next"), ("Previous", "previous"), ("Vol+", "volume_up"), ("Vol-", "volume_down"), ("Mute", "mute")]:
            tk.Button(buttons, text=label, command=lambda a=action: self.send("media", a)).pack(side="left", padx=2)
        tk.Button(buttons, text="Present Next", command=lambda: self.send("presentation", "next")).pack(side="left", padx=2)
        tk.Button(buttons, text="Present Prev", command=lambda: self.send("presentation", "previous")).pack(side="left", padx=2)

        keys = tk.LabelFrame(root, text="Keyboard")
        keys.pack(fill="x", padx=10, pady=5)
        self.text = tk.Entry(keys)
        self.text.pack(fill="x", padx=8, pady=5)
        self.text.bind("<KeyPress>", self.key_press)
        for key in ["ENTER", "BACKSPACE", "ESC", "SHIFT", "CTRL", "ALT", "UP", "DOWN", "LEFT", "RIGHT"]:
            tk.Button(keys, text=key, command=lambda k=key: self.send_key(k)).pack(side="left", padx=2, pady=4)

        bottom = tk.Frame(root)
        bottom.pack(fill="x", padx=10, pady=8)
        tk.Button(bottom, text="Ping", command=self.ping).pack(side="left")
        tk.Button(bottom, text="Get Host Info", command=self.get_info).pack(side="left", padx=5)
        self.latency = tk.Label(bottom, text="Latency: -")
        self.latency.pack(side="left", padx=15)
        self.log = tk.Text(root, height=7, state="disabled")
        self.log.pack(fill="both", expand=True, padx=10, pady=5)
        root.after(100, self.poll)

    def write_log(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def discover(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(1.5)
            sock.sendto(b"SMARTDESK_DISCOVER", ("255.255.255.255", DISCOVERY_PORT))
            data, _ = sock.recvfrom(4096)
            result = json.loads(data.decode())
            self.ip.delete(0, "end")
            self.ip.insert(0, result["ip"])
            self.port.delete(0, "end")
            self.port.insert(0, str(result["port"]))
            self.write_log(f"Discovered {result['hostname']} at {result['ip']}:{result['port']}")
            sock.close()
        except Exception:
            self.write_log("Unable to discover SmartDesk host. Enter the host IP manually.")

    def connect(self):
        if self.sock:
            return
        try:
            self.sock = socket.create_connection((self.ip.get().strip(), int(self.port.get())), timeout=5)
            self.sock.settimeout(1)
            self.running = True
            self.reader_thread = threading.Thread(target=self.read_loop, daemon=True)
            self.reader_thread.start()
            self.status.config(text="Connected / not paired")
            if self.token:
                self.send_raw(self.message("auth", "resume", {"token": self.token}))
            self.write_log("TCP connection established")
        except Exception as exc:
            self.sock = None
            messagebox.showerror("Connection failed", str(exc))

    def read_loop(self):
        buffer = b""
        while self.running and self.sock:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                buffer += data
                while b"\n" in buffer:
                    line, buffer = buffer.split(b"\n", 1)
                    if line:
                        self.responses.put(json.loads(line.decode()))
            except socket.timeout:
                continue
            except Exception:
                break
        self.running = False
        self.responses.put({"_closed": True})

    def send_raw(self, message):
        if not self.sock or not self.running:
            self.write_log("Not connected")
            return None
        self.sock.sendall((json.dumps(message, separators=(",", ":")) + "\n").encode())
        return message["id"]

    def send(self, msg_type, action, data=None):
        if not self.token:
            self.write_log("Pair the controller first")
            return
        msg = self.message(msg_type, action, data or {})
        self.send_raw(msg)

    def message(self, msg_type, action, data):
        msg = {"version": PROTOCOL_VERSION, "id": str(self.next_id), "type": msg_type, "action": action, "data": data}
        self.next_id += 1
        if self.token:
            msg["token"] = self.token
        return msg

    def pair(self):
        if not self.sock:
            self.connect()
        if not self.sock:
            return
        msg = self.message("auth", "pair", {"code": self.code.get().strip()})
        self.send_raw(msg)

    def get_info(self):
        self.send("system", "get_host_info")

    def ping(self):
        if not self.token:
            self.write_log("Pair the controller first")
            return
        msg = self.message("system", "ping")
        self.pending_ping = time.perf_counter()
        self.send_raw(msg)

    def send_key(self, key):
        self.send("keyboard", "press", {"key": key})
        self.send("keyboard", "release", {"key": key})

    def key_press(self, event):
        if event.keysym in {"Shift_L", "Control_L", "Alt_L", "Return", "BackSpace", "Escape", "space", "Up", "Down", "Left", "Right"}:
            mapping = {"Shift_L": "SHIFT", "Control_L": "CTRL", "Alt_L": "ALT", "Return": "ENTER", "BackSpace": "BACKSPACE", "Escape": "ESC", "space": "SPACE", "Up": "UP", "Down": "DOWN", "Left": "LEFT", "Right": "RIGHT"}
            self.send_key(mapping[event.keysym])
        elif event.char and event.char.isprintable():
            self.send("keyboard", "press", {"key": event.char})
            self.send("keyboard", "release", {"key": event.char})

    def mouse_move(self, event):
        if not hasattr(self, "last_mouse"):
            self.last_mouse = (event.x, event.y)
            return
        x, y = self.last_mouse
        dx, dy = event.x - x, event.y - y
        self.last_mouse = (event.x, event.y)
        if self.token and (dx or dy):
            self.send("mouse", "move", {"dx": dx, "dy": dy})

    def mouse_scroll(self, event):
        self.send("mouse", "scroll", {"dx": 0, "dy": 1 if event.delta > 0 else -1})

    def disconnect(self):
        self.running = False
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
        self.sock = None
        self.status.config(text="Disconnected")
        self.write_log("Disconnected")

    def poll(self):
        try:
            while True:
                response = self.responses.get_nowait()
                if response.get("_closed"):
                    self.status.config(text="Disconnected")
                    continue
                if response.get("type") == "state":
                    state = response.get("state", "UNKNOWN")
                    if state == "AUTHENTICATING":
                        self.status.config(text="Connected / not paired")
                    elif state == "AUTHENTICATED":
                        self.status.config(text="Authenticated")
                    else:
                        self.status.config(text=state)
                    self.write_log(f"Server state: {state}")
                    continue
                if response.get("status") == "ok":
                    data = response.get("data", {})
                    if "token" in data:
                        self.token = data["token"]
                        self.status.config(text="Authenticated")
                        self.write_log("Pairing successful")
                    if "pong_ns" in data and hasattr(self, "pending_ping"):
                        ms = (time.perf_counter() - self.pending_ping) * 1000
                        self.latency.config(text=f"Latency: {ms:.2f} ms")
                    if "os" in data:
                        self.info.config(text=" | ".join(f"{k}: {v}" for k, v in data.items()))
                else:
                    self.write_log(f"Error: {response.get('error', response)}")
        except queue.Empty:
            pass
        self.root.after(100, self.poll)


if __name__ == "__main__":
    root = tk.Tk()
    SmartDeskClient(root)
    root.mainloop()
