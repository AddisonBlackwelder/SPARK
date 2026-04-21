# hub.py — Raspberry Pi Pico 2W (HUB / SERVER)
# Hosts its own WiFi access point — no router or internet required.
# Client Picos connect directly to the hub's network.
#
# Flash this as code.py on the hub Pico.
# The hub AP IP is always 192.168.4.1 — set HUB_IP to this on all client Picos.

import wifi
import socketpool
import time

# ── Network config ────────────────────────────────────────────────────────────

AP_SSID       = "SPARK_HUB"       # Network name client Picos will connect to
AP_PASSWORD   = "sparkpass"        # Min 8 characters; set to "" for open network
AP_IP         = "192.168.4.1"      # Fixed — this is always the AP gateway IP
HOST          = "0.0.0.0"          # Listen on all interfaces
PORT          = 5000
MAX_CLIENTS   = 5

# ── State ─────────────────────────────────────────────────────────────────────

clients  = []   # list of (socket, address, recv_buffer) tuples
_pool    = None
_server  = None

# ── WiFi AP ───────────────────────────────────────────────────────────────────

def start_ap():
    global _pool
    print(f"[AP] Starting access point '{AP_SSID}' ...")
    wifi.radio.start_ap(ssid=AP_SSID, password=AP_PASSWORD)
    _pool = socketpool.SocketPool(wifi.radio)
    print(f"[AP] Access point up — clients should connect to '{AP_SSID}'")
    print(f"[AP] Hub IP: {AP_IP}  (set HUB_IP = \"{AP_IP}\" on all client Picos)")

# ── Server ────────────────────────────────────────────────────────────────────

def start_server():
    global _server
    _server = _pool.socket(_pool.AF_INET, _pool.SOCK_STREAM)
    _server.setsockopt(_pool.SOL_SOCKET, _pool.SO_REUSEADDR, 1)
    _server.bind((HOST, PORT))
    _server.listen(MAX_CLIENTS)
    _server.settimeout(0)   # non-blocking accept
    print(f"[Hub] Listening on port {PORT} (max {MAX_CLIENTS} clients)")

# ── Broadcast / send ──────────────────────────────────────────────────────────

def broadcast(message: str, exclude=None):
    """
    Send a string to every connected client.

    Args:
        message : Plain text (newline appended automatically)
        exclude : Optional client socket to skip (e.g. the sender)
    """
    print(f"[Hub] Sending message: {message}")
    if not message.endswith("\n"):
        message += "\n"
    data = message.encode("utf-8")
    dead = []
    for sock, addr, _ in clients:
        if sock is exclude:
            continue
        try:
            sock.send(data)
        except OSError:
            print(f"[Hub] Client {addr} unreachable — marking for removal.")
            dead.append(sock)
    _remove_dead(dead)


def send_to(client_index: int, message: str):
    """
    Send a string to a single client by its index in the clients list.

    Args:
        client_index : Index into the clients list
        message      : Plain text string
    """
    if client_index >= len(clients):
        print(f"[Hub] No client at index {client_index}.")
        return
    sock, addr, _ = clients[client_index]
    if not message.endswith("\n"):
        message += "\n"
    try:
        sock.send(message.encode("utf-8"))
    except OSError as e:
        print(f"[Hub] Send to {addr} failed: {e}")
        _remove_dead([sock])

# ── Receive helpers ───────────────────────────────────────────────────────────

def _remove_dead(dead_socks):
    global clients
    for ds in dead_socks:
        clients = [(s, a, b) for s, a, b in clients if s is not ds]
        try:
            ds.close()
        except OSError:
            pass


_recv_buf = bytearray(256)   # reusable read buffer

def _poll_clients():
    """
    Non-blocking read from every client.
    Returns list of (address, message_string) for each complete line received.
    """
    received = []
    dead     = []

    for i, (sock, addr, buf) in enumerate(clients):
        try:
            nbytes = sock.recv_into(_recv_buf, 256)
            if nbytes == 0:
                print(f"[Hub] Client {addr} disconnected.")
                dead.append(sock)
                continue
            if nbytes > 0:
                clients[i] = (sock, addr, buf + _recv_buf[:nbytes].decode("utf-8"))
        except OSError:
            pass   # EAGAIN / EWOULDBLOCK — nothing to read yet

        # Extract complete lines from this client's buffer
        while "\n" in clients[i][2]:
            line, rest = clients[i][2].split("\n", 1)
            clients[i] = (clients[i][0], clients[i][1], rest)
            msg = line.strip()
            if msg:
                received.append((addr, msg))

    _remove_dead(dead)
    return received


def _accept_new():
    """Accept up to one new client per call (non-blocking)."""
    global clients
    try:
        sock, addr = _server.accept()
        sock.settimeout(0)
        clients.append((sock, addr, ""))
        print(f"[Hub] New client connected: {addr}  (total: {len(clients)})")
    except OSError:
        pass   # no pending connection


# ── on_message callback ───────────────────────────────────────────────────────

def on_message(addr, message: str):
    """
    Called whenever a complete message arrives from a client.
    Override or extend this to handle specific commands.

    Current behaviour:
      HELLO        → acknowledged, broadcast join notice to other clients
      SWITCH:N:V   → broadcast switch state to all other clients
      anything else → print and echo back
    """
    print(f"[MSG] {addr}: {message}")

    if message == "HELLO":
        # Find the sender's socket to echo directly
        sender = next((s for s, a, _ in clients if a == addr))
        if sender:
            try:
                sender.send(b"HELLO:ACK\n")
            except OSError:
                pass
        broadcast(f"JOIN:{addr[0]}", exclude=sender)

    elif message.startswith("SWITCH:"):
        # Forward switch state changes to all other clients
        sender = next((s for s, a, _ in clients if a == addr))
        broadcast(message, exclude=sender)

    else:
        # Unknown message — echo it back and log it
        sender = next((s for s, a, _ in clients if a == addr))
        if sender:
            try:
                sender.send(f"ECHO:{message}\n".encode("utf-8"))
            except OSError:
                pass


# ── Main loop ─────────────────────────────────────────────────────────────────

start_ap()
start_server()

print("[Hub] Running. Waiting for clients ...")

while True:
    _accept_new()

    for addr, msg in _poll_clients():
        on_message(addr, msg)

    broadcast("DISPLAY: HELLO!")

    time.sleep(10)   # ~50 Hz poll rate