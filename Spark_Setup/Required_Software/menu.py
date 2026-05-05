# menu.py — Raspberry Pi Pico
# Menu item types and the Menu class
#
# Buttons (adjust pins if needed):
#   UP     → GP2
#   DOWN   → GP3
#   SELECT → GP4
#   BACK   → GP5

import displayio, terminalio, board, digitalio
import time
import main_loop
from adafruit_display_text import label
from display import colors
from time import sleep

# ── Button pins ───────────────────────────────────────────────────────────────

BTN_UP     = board.GP20
BTN_DOWN   = board.GP27
BTN_SELECT = board.GP22
BTN_BACK   = board.GP21

DEBOUNCE   = 0.2   # seconds between button reads

# ── Menu item types ───────────────────────────────────────────────────────────

class Action:
    """Runs a function when selected."""
    def __init__(self, name, fn):
        self.name = name
        self.fn   = fn

    def select(self):
        self.fn()
        return None


class Toggle:
    """On/off setting. SELECT flips the value."""
    def __init__(self, name, value=False):
        self.name  = name
        self.value = value

    def select(self):
        self.value = not self.value
        return None


class Number:
    """Integer setting. SELECT increments, wraps at max back to min."""
    def __init__(self, name, value=0, min_val=0, max_val=10, step=1, unit=""):
        self.name    = name
        self.value   = value
        self.min_val = min_val
        self.max_val = max_val
        self.step    = step
        self.unit    = unit

    def select(self):
        self.value += self.step
        if self.value > self.max_val:
            self.value = self.min_val
        return None


class Submenu:
    """Opens a nested list of items."""
    def __init__(self, name, items):
        self.name  = name
        self.items = items

    def select(self):
        return self.items   # Menu will push this list onto the stack


class Image:
    """Displays a .bmp image when selected. Press BACK to return to the menu."""
    def __init__(self, name, filepath):
        self.name     = name
        self.filepath = filepath

    def select(self):
        return self.filepath   # Menu will detect a string and show the image


# ── Menu class ────────────────────────────────────────────────────────────────

class Menu:
    TITLE_H  = 16
    ROW_H    = 16
    MAX_ROWS = (131 - TITLE_H) // ROW_H   # 7 rows visible

    def __init__(self, display):
        """Pass in a Display instance from display.py."""
        self.display = display
        self.mirrored_switches = []

        # Set up buttons
        self._up     = self._btn(BTN_UP)
        self._down   = self._btn(BTN_DOWN)
        self._select = self._btn(BTN_SELECT)
        self._back   = self._btn(BTN_BACK)
        print(f"[INFO] Successfully initalized display and menu")

    def _btn(self, pin):
        b = digitalio.DigitalInOut(pin)
        b.direction = digitalio.Direction.INPUT
        b.pull = digitalio.Pull.UP   # LOW = pressed
        return b
    
    def add_mirror(self, input_pin, output_pin):
        
        _input = digitalio.DigitalInOut(input_pin)
        _input.direction = digitalio.Direction.INPUT
        _input.pull = digitalio.Pull.DOWN
        
        _output = digitalio.DigitalInOut(output_pin)
        _output.direction = digitalio.Direction.OUTPUT
        _output.value = False
        
        print(f"[INFO] Added switch mirror: {input_pin} --> {output_pin}")
        self.mirrored_switches.append((_input, _output))
    
    def mirror_switches(self):
        for inp, out in self.mirrored_switches:
            out.value = inp.value

    # ── Drawing ───────────────────────────────────────────────────────────────

    def _rect(self, color, x, y, w, h):
        bmp = displayio.Bitmap(w, h, 1)
        pal = displayio.Palette(1)
        pal[0] = color
        return displayio.TileGrid(bmp, pixel_shader=pal, x=x, y=y)

    def _lbl(self, text, color, x, y):
        return label.Label(terminalio.FONT, text=text, color=color, x=x, y=y)

    def _draw(self, title, items, selected, scroll):
        W = self.display.W
        root = displayio.Group()

        # Background + header
        root.append(self._rect(colors['cyan'], 0, 13, W, 1))
        root.append(self._lbl(title, colors['cyan'], 4, 7))

        # Rows
        for i, item in enumerate(items[scroll: scroll + self.MAX_ROWS]):
            abs_i  = scroll + i
            is_sel = abs_i == selected
            y      = self.TITLE_H + i * self.ROW_H

            if is_sel:
                root.append(self._rect(0x0F2035, 0, y - 2, W, self.ROW_H - 2))
                root.append(self._lbl(">", colors['cyan'], 1, y + 4))

            root.append(self._lbl(
                item.name[:12],
                colors['cyan'] if is_sel else colors['white'],
                10, y + 4
            ))

            # Right-side value indicators
            if isinstance(item, Toggle):
                val, col = (" ON", colors['green']) if item.value else ("OFF", colors['red'])
                root.append(self._lbl(val, col, W - 22, y + 4))

            elif isinstance(item, Number):
                val = str(item.value) + item.unit
                root.append(self._lbl(val[-5:], colors['amber'], W - len(val[-5:]) * 6 - 2, y + 4))

            elif isinstance(item, Submenu):
                root.append(self._lbl(">", colors['grey'], W - 10, y + 4))

            elif isinstance(item, Image):
                root.append(self._lbl("[]", colors['grey'], W - 14, y + 4))

        self.display.display.root_group = root

    # ── Scroll helper ─────────────────────────────────────────────────────────

    def _draw_ascii(self, content):
        """Render multiline ASCII text centered on screen."""
        CHAR_W = 6    # terminalio.FONT character width  (pixels)
        CHAR_H = 12   # terminalio.FONT character height (pixels)
        PAD    = 3    # pixels from left edge

        root  = displayio.Group()
        root.append(self._rect(0x0A0A1A, 0, 0, self.display.W, self.display.H))

        lines = content.split("\n")

        # Total text block height — used to vertically centre the block
        total_h = len(lines) * CHAR_H
        start_y = max(2, (self.display.H - total_h) // 2)

        for i, line in enumerate(lines):
            y = start_y + i * CHAR_H
            if y + CHAR_H > self.display.H:
                break   # don't draw off screen

            # First line treated as a title — highlight in cyan
            color = colors['cyan'] if i == 0 else colors['white']

            # Centre-align if line starts with a space (header rows)
            if line.startswith(" ") or "|" not in line:
                x = max(PAD, (self.display.W - len(line) * CHAR_W) // 2)
            else:
                x = PAD

            root.append(self._lbl(line, color, x, y))

        # Hint at bottom
        hint = "BACK to return"
        hx   = (self.display.W - len(hint) * CHAR_W) // 2
        root.append(self._lbl(hint, colors['grey'], hx, self.display.H - 10))

        self.display.display.root_group = root

    def _scroll_to(self, frame):
        sel, sc = frame[2], frame[3]
        if sel < sc:
            frame[3] = sel
        elif sel >= sc + self.MAX_ROWS:
            frame[3] = sel - self.MAX_ROWS + 1

    # ── Run ───────────────────────────────────────────────────────────────────

    def show(self, title, items):
        """
        Show the menu and block until the user backs out of the root level.

        Args:
            title : string shown in the header
            items : list of Action / Toggle / Number / Submenu objects
        """
        stack = [[title, items, 0, 0]]
        last  = 0

        while stack:
            f = stack[-1]
            self._draw(f[0], f[1], f[2], f[3])

            now = time.monotonic()
            if now - last < DEBOUNCE:
                sleep(0.02)
                continue

            if not self._up.value:
                print("[INFO] Up pressed")
                f[2] = (f[2] - 1) % len(f[1])
                self._scroll_to(f)
                last = now

            elif not self._down.value:
                print("[INFO] Down pressed")
                f[2] = (f[2] + 1) % len(f[1])
                self._scroll_to(f)
                last = now

            elif not self._select.value:
                print("[INFO] Select pressed")
                result = f[1][f[2]].select()
                if isinstance(result, list):
                    # Submenu — push new frame
                    stack.append([f[1][f[2]].name, result, 0, 0])
                elif isinstance(result, str):
                    # Image — show it until BACK is pressed
                    self.display.image(result)
                    while not self._back.value:
                        sleep(0.02)
                    sleep(DEBOUNCE)
                    while self._back.value:
                        sleep(0.02)
                last = now

            elif not self._back.value:
                print("[INFO] Back pressed")
                if len(stack) > 1:
                    stack.pop()
                    last = now
            
            main_loop.tick(self)