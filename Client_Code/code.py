import board
from menu_options import main_menu
from display import Display
from menu import Menu, Action, Toggle, Number, Submenu
from time import sleep
import internet

# ── Network config ────────────────────────────────────────────────────────────

WIFI_SSID     = "SPARK_HUB"      # Must match AP_SSID in hub.py
WIFI_PASSWORD = "sparkpass"       # Must match AP_PASSWORD in hub.py
HUB_IP        = "192.168.4.1"    # Fixed AP gateway — never changes
HUB_PORT      = 5000

# ── Switch mirrors ────────────────────────────────────────────────────────────

pin_pairs = [
    (board.GP0, board.GP1),
    (board.GP2, board.GP3),
    (board.GP4, board.GP5),
    (board.GP6, board.GP7),
    (board.GP8, board.GP9),
]

# ── Startup ───────────────────────────────────────────────────────────────────

screen = Display()
menu   = Menu(screen)

for _in, _out in pin_pairs:
    menu.add_mirror(_in, _out)

screen.text("Connecting\nto hub AP...", color="white")
wifi_ok = internet.connect_wifi(WIFI_SSID, WIFI_PASSWORD)
 
if wifi_ok:
    screen.text("WiFi OK\nConnecting\nto hub...", color="green")
    hub_ok = internet.connect_hub(HUB_IP, HUB_PORT)
    if hub_ok:
        screen.text("Hub OK!", color="green")
        internet.send("HELLO")   # announce ourselves to the hub
    else:
        screen.text("Hub offline.\nRunning local.", color="amber")
else:
    screen.text("WiFi failed.\nRunning local.", color="red")
 
sleep(1.5)

# ── Main menu ─────────────────────────────────────────────────────────────────

menu.show("MENU      S.P.A.R.K.", main_menu)