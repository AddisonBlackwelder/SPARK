import board
import digitalio

def init():
    #input, output
    pin_pairs = [
        (board.GP1, board.GP0),
        ]
    mirrored_switches = []
        
    for input_pin, output_pin in pin_pairs:
        _input = digitalio.DigitalInOut(input_pin)
        _input.direction = digitalio.Direction.INPUT
        _input.pull = digitalio.Pull.DOWN
        
        _output = digitalio.DigitalInOut(output_pin)
        _output.direction = digitalio.Direction.OUTPUT
        _output.value = False
        mirrored_switches.append((_input, _output))
        
        print(f"[INFO] Added switch mirror: {input_pin} --> {output_pin}")

def update(self):
    for inp, out in self.mirrored_switches:
        out.value = inp.value