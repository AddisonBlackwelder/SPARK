# internet.py — Raspberry Pi Pico 2W (CLIENT)
# Handles WiFi connection and TCP socket comms with the hub Pico.
#
# Usage in code.py:
#   import internet
#   internet.connect_wifi(SSID, PASSWORD)
#   internet.connect_hub(HUB_IP, HUB_PORT)
#   internet.send("hello\n")
#   msg = internet.receive()   # returns str or None (non-blocking)
#   internet.disconnect()

import wifi
import socketpool
import time

# ── Module-level state ────────────────────────────────────────────────────────

_pool   = None   # socketpool.SocketPool
_sock   = None   # TCP socket to hub
_buf    = ""     # incomplete-line accumulation buffer

# ── Public API ────────────────────────────────────────────────────────────────

def connect_wifi(ssid: str, password: str, retries: int = 5, retry_delay: float = 2.0) -> bool:
    """
    Join the WiFi network.  Returns True on success, False after all retries.

    Args:
        ssid        : Network name
        password    : Network password
        retries     : How many connection attempts before giving up
        retry_delay : Seconds to wait between attempts
    """
    global _pool

    print(f"[WiFi] Connecting to '{ssid}' ...")

    for attempt in range(1, retries + 1):
        try:
            wifi.radio.connect(ssid, password)
            _pool = socketpool.SocketPool(wifi.radio)
            print(f"[WiFi] Connected — IP: {wifi.radio.ipv4_address}")
            return True
        except Exception as e:
            print(f"[WiFi] Attempt {attempt}/{retries} failed: {e}")
            if attempt < retries:
                time.sleep(retry_delay)

    print("[WiFi] Could not connect to WiFi.")
    return False


def connect_hub(host: str, port: int, retries: int = 5, retry_delay: float = 2.0) -> bool:
    """
    Open a TCP socket to the hub Pico server.  Returns True on success.

    Args:
        host        : Hub Pico IP address (e.g. "192.168.1.50")
        port        : Port the hub is listening on (e.g. 5000)
        retries     : How many connection attempts before giving up
        retry_delay : Seconds to wait between attempts
    """
    global _pool, _sock

    if _pool is None:
        print("[Hub] WiFi not connected — call connect_wifi() first.")
        return False

    print(f"[Hub] Connecting to hub at {host}:{port} ...")

    for attempt in range(1, retries + 1):
        try:
            _sock = _pool.socket(_pool.AF_INET, _pool.SOCK_STREAM)
            _sock.settimeout(0)          # non-blocking from here on
            _sock.connect((host, port))
            print("[Hub] Connected to hub.")
            return True
        except OSError as e:
            # EINPROGRESS (errno 119) is normal for non-blocking connect
            if hasattr(e, "errno") and e.errno == 119:
                print("[Hub] Connected to hub (non-blocking).")
                return True
            print(f"[Hub] Attempt {attempt}/{retries} failed: {e}")
            _sock = None
            if attempt < retries:
                time.sleep(retry_delay)

    print("[Hub] Could not connect to hub.")
    return False


def send(message: str) -> bool:
    """
    Send a string to the hub.  A newline is appended automatically if missing.
    Returns True if the data was written to the socket, False on error.

    Args:
        message : Plain text string to send (e.g. "SWITCH:0:1")
    """
    global _sock

    if _sock is None:
        print("[Hub] Not connected — cannot send.")
        return False

    if not message.endswith("\n"):
        message += "\n"

    try:
        _sock.send(message.encode("utf-8"))
        return True
    except OSError as e:
        print(f"[Hub] Send error: {e}")
        return False


_recv_buf = bytearray(256)   # reusable read buffer

def receive() -> str | None:
    """
    Non-blocking poll for incoming data from the hub.
    Returns a complete message string (newline stripped) when one arrives,
    or None if nothing is ready yet.

    Call this regularly from your main loop / tick function.
    """
    global _sock, _buf

    if _sock is None:
        return None

    try:
        nbytes = _sock.recv_into(_recv_buf, 256)
        if nbytes > 0:
            _buf += _recv_buf[:nbytes].decode("utf-8")
    except OSError:
        # EAGAIN / EWOULDBLOCK — nothing waiting, that's fine
        pass

    # Return the first complete line if we have one
    if "\n" in _buf:
        line, _buf = _buf.split("\n", 1)
        return line.strip()

    return None


def disconnect():
    """Close the TCP socket cleanly."""
    global _sock

    if _sock:
        try:
            _sock.close()
        except OSError:
            pass
        _sock = None
        print("[Hub] Disconnected.")


def is_connected() -> bool:
    """Return True if the TCP socket is open."""
    return _sock is not None