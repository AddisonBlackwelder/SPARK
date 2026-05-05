import board
from menu_options import main_menu
from display import Display
from menu import Menu, Action, Toggle, Number, Submenu
from time import sleep

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
    (board.GP10, board.GP11),
    (board.GP12, board.GP13),
    (board.GP14, board.GP15),
    ]

# ── Startup ───────────────────────────────────────────────────────────────────

screen = Display()
menu   = Menu(screen)

for in_pin, out_pin in pin_pairs:
    menu.add_mirror(out_pin, in_pin)

# ── Main menu ─────────────────────────────────────────────────────────────────

menu.show("MENU      S.P.A.R.K.", main_menu)