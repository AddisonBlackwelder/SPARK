from time import sleep
import board, digitalio, switches

tick_rate = 0.02

def tick(menu):
    menu.mirror_switches()
    sleep(tick_rate)