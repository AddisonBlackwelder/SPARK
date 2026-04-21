
def init():
    #input, output
    pin_pairs = [
        (board.GP0, board.GP1),
        (board.GP2, board.GP3),
        (board.GP4, board.GP5),
        (board.GP6, board.GP7),
        (board.GP14, board.GP15),
        ]
        
    for input_pin, output_pin in pin_pairs:
        _input = digitalio.DigitalInOut(input_pin)
        _input.direction = digitalio.Direction.INPUT
        _input.pull = digitalio.Pull.DOWN
        
        _output = digitalio.DigitalInOut(output_pin)
        _output.direction = digitalio.Direction.OUTPUT
        _output.value = False
        
        print(f"[INFO] Added switch mirror: {input_pin} --> {output_pin}")

def update(self):
    for inp, out in self.mirrored_switches:
        out.value = inp.value