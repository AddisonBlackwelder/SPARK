## All code here is for the pico placed on the board

### code.py
This code will run on bootup. Will init screen, menu, and pins (for pin mirroring)

### display.py
Used for any display related code

### main_loop.py
This function is run every 20ms roughly. Its run after the display checks for updates

### menu_options.py
This is what constructs the menu. Everything is done using python arrays

### menu.py
This is the big boy file. Used for anything menu related.
Everything is done using classes. There are 5 different options for menu items:
- Action = runs a function
- Toggle = Has a binary value that is toggled when clicked
- Number = Can be a range of numbers where each time it is clicked, the value changes by *step* and can range from *min* to *max*
- Submenu = Opens a submenu and adds old menu to stack
- Image = Will display a image on the screen and will stay until back button is pressed