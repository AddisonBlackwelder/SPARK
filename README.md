### Team 42 SPARK - Software

Code is split into two types, client and hub. the client code gets flased onto the pico that is connected to the board and the teacher code gets flashed onto a pico that connects via USB to the teachers laptop.
At the time of design day, everything functions as follows:

1. Hub starts us first to give ample time for system to boot
1. Client starts up and attempts to connect to a wifi access point provided by the hub
    * Connection Succsessful - Client sends a hello message and waits for an ACK from hub
    * Connection Failure - Client continues without hub connection :(
1. Client boots up display and menu
1. Starting now the teacher can send a message to the students using the broadcast functions
    * I wish I could have done this message sending via USB to the hub so it knows what to send. As of now it will have to be preprogrammed with what to send after boot.
1. Both picos sit in a while loop doing simple processing