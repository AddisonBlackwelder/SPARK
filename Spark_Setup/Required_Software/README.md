## All code here is for the pico placed on the board

### code.py
This python script will run once as board starts up. It is responsible for initalizing all network usage and pin pairs for switch mirroring. If you would like to change any IPs or ports, this is the file to mess with.

### display.py
This file is what drives the display. It defines a class that is used to add text and images to the display as we see fit. This is also where we defines what pins are used to communicate with the display. The functions can be called by the user if they would like to add JUST text, or a an image. A more user friendly version of these functions can be found in menu.py.
P.S. The display currently updates all the time. I couldn't quite figure out a variable refresh rate. I assume this would greatly reduce power consuption.

### main_loop.py
This script runs every tick_rate second(s). Changing the value at the top of this value chages how often the Pico checks for updates within the system; levers changing status, buttons pressed, display updating.

### menu_options.py
If you would like to add more menu options to the screen, this is the file you should change. Everything is done using simple python arrays. All of the different menu options can be found in menu.py, they are also explained below.

### menu.py
This is the big boy file. Used for anything menu related.
Everything is done using classes. There are currently 5 different options for menu items. Below is each option as well as an example.

- Action = Runs a function when selected
	- Check battery level using custom a function.
- Toggle = Changes a binary value (true or false) when toggled.
	- WiFi enabled or disabled.
- Number = Can be a range of numbers where each time it is clicked, the value changes by *step* and can range from *min* to *max*
	- Display brightness level (Not implemented)
- Submenu = Opens a sub menu and adds old menu to stack
	- List of possible projects
- Image = Will display an image on the screen and will stay until back button is pressed\
	- Picture of current project
The menu is processed using a stack. Anytime the user enters a sub menu, it is noted on the stack. When the user would like to move back a menu, we pop the latest item from the stack.