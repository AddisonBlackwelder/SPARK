### Team 42 SPARK - Software

There are two folders in this repo:
- Spark_Setup - These files NEED to be added to each pico that are on the boards. The .uf2 file allows to python code to be run on your pico while the ./Required_Software folder contains the software that allows the LEDs below each switch to change as well as also driving the display.

- Optional_Internet_Hub - If you choose to not setup the teacher hub software, this folder can be ignored. This software is used by flashing onto a separate pico that will attempt to connect to all student boards it finds close by. The teacher can then use this connection to commutation with the students by controlling their boards.
	
These folders are explained more once clicked on above.
	
### TO DOWNLOAD AND USE CONTENT

Please see the releases tab on the right side of your screen. This should download a zip folder that contains folders of code that needs to be flashed to the teacher and student picos. To flash code to the pico, please follow the directions below:

1. Download ZIP folder as shown above.
1. Unzip the folder to an easy to access location.
1. Open Spark_Setup and locate the .uf2 file.
1. Plug your pico into your computer while holding the only button on the top of the Pico. This should open file explorer on your computer screen.
	- If nothing opens, open File Explorer manually and look for a drive called RPI-RP2.
1. Copy the file stored at Spark_Setup/Firmware/ and copy it to the folder that popped up after plugging in your pico.
1. Unplug your pico, wait a few seconds, then plug back in WITHOUT holding the button.
1. Copy all files in Spark_Setup/Software/ to the new window that opens
1. Unplug Pico and place on board.
1. Turn board on, everything should come to life!
	- If it does not work, restart from step 1.
