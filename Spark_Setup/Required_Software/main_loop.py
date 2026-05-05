from time import sleep

tick_rate = 0.02

# Feel free to add anything to this function that you would like processed
def tick(menu):
    menu.mirror_switches()
    sleep(tick_rate)