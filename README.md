### Team 42 SPARK - Software

There are two folders in this repo:
- Spark_Setup - These files NEED to be added to each pico that are on the boards. This software allows the LEDs below each flip switch to change based on switch state. This software also drives the display on the board.
- Optional_Internet_Hub - If you choose to not setup the teacher hub spftware, this folder can be ignored. This software is used by flashing onto a seperate pico that will attempt to connect to all student boards it finds closeby. The teacher can then use this connection to commucation with the students by controlling their boards.
	
These folders are explained more once clicked on above.
	
### TO DOWNLOAD AND USE CONTENT

Please see the releases tab on the right side of your screen. This should download a zip folder that contains folders of code that needs to be flashed to the teacher and student picos. To flash code to the pico, please follow the directions below:

1. Download ZIP folder as shown above.
1. Unzip the folder to an eazy to access location.
1. Go to Spark_Setup -> Firmware and grab the only file in this folder.
1. Plug your Pico into your computer while holding the only button on the top of the Pico. This should open file explorer on your computer screen.
1. Copy the file stored at Spark_Setup/Firmware/ and copy it to the folder that popped up after plugging in your pico.
1. Unplug your pico and then plug back in WITHOUT holding the button.
1. Copy all files in Spark_Setup/Software to the new window that opens
1. Unplug Pico and place on board.
1. Turn board on, everything should come to life!
