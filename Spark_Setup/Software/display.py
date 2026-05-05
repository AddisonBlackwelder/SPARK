# Raspberry Pi Pico

from time import sleep
from adafruit_st7735r import ST7735R
import displayio, busio, terminalio
import board
from fourwire import FourWire
from adafruit_display_text import label

colors = {
    'white'  : 0xFFFFFF,
    'blue'   : 0xFF0000,
    'green'  : 0x00FF00,
    'purple' : 0x800080,
    'red'    : 0x0000FF,
    'cyan'   : 0xFFCC00,
    'amber'  : 0x00AAFF,
    'grey'   : 0x665544,
}

class Display:
    
    W = 130		#width and height of display
    H = 131
    
    def __init__(self):
        self.mosi_pin = board.GP19	#Yellow Wire or SDA
        self.clk_pin = board.GP18	#Black Wire or SCL
        self.reset_pin = board.GP17 #Orange Wire 
        self.cs_pin = board.GP26	#Blue Wire 
        self.dc_pin = board.GP16    #Green Wire 

        # Display init
        displayio.release_displays()
        spi = busio.SPI(self.clk_pin, self.mosi_pin)
        display_bus = FourWire(spi, command=self.dc_pin, chip_select=self.cs_pin, reset=self.reset_pin)
        self.display = ST7735R(display_bus, width=130, height=131, bgr=1)
        
        # Create display group
        self.splash = displayio.Group()
        self.text_area = label.Label(terminalio.FONT, text="", color=colors['white'], x=4, y=12)
        self.splash.append(self.text_area)
        self.display.root_group = self.splash

    def text(self, text:str, speed:float=None, color=None):
        if color:
            if color in colors:
                self.text_area.color = colors[color]
            else:
                self.text_area.color = color
        if speed:
            for i in range(len(text)):
                self.text_area.text = text[:i+1]
                sleep(speed)
            return
        self.text_area.text = text
        return
    
    def image(self, filepath:str):
        bitmap, palette = displayio.OnDiskBitmap(filepath), None
        bitmap = displayio.OnDiskBitmap(filepath)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
        
        splash = displayio.Group()
        splash.append(tile_grid)
        self.display.root_group = splash
        return






