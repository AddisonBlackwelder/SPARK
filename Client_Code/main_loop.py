from time import sleep, monotonic
import board, digitalio, internet

tick_rate = 0.02
SEND_BTN = board.GP15
DEBOUNCE_MS = 500

_last_state = True
_last_change = 0.0
_last_tick = 0.0

b = digitalio.DigitalInOut(SEND_BTN)
b.direction = digitalio.Direction.INPUT
b.pull = digitalio.Pull.UP   # LOW = pressed

def tick(menu):
    menu.mirror_switches()
    sleep(tick_rate)
    msg = internet.receive()
    if msg:
        _handle_hub_message(msg, menu)
 
 
def _handle_hub_message(msg: str, menu):
    """
    Dispatch messages received from the hub.
 
    Protocol (extend as needed):
      PING              → reply with PONG
      CMD:<command>     → reserved for hub-initiated commands
      BROADCAST:<text>  → log/display hub broadcast
    """
    print(f"[Hub→Client] {msg}")
 
    if msg == "PING":
        internet.send("PONG")
 
    elif msg.startswith("CMD:"):
        command = msg[4:]
        print(f"[CMD] Received command: {command}")
        # TODO: dispatch commands to menu actions here
 
    elif msg.startswith("DISPLAY:"):
        text = msg[10:]
        # Optionally push text to the display:
 
    elif msg.startswith("HELLO:ACK"):
        print("[Hub] Handshake acknowledged.")
 
    else:
        print(f"[Hub] Unknown message: {msg}")
    pass