from time import sleep
import board, digitalio, switches

tick_rate = .02

def tick(menu):
    menu.mirror_switches()
    sleep(tick_rate)