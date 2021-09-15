## Installing WLED on SP511E Controller

The SP511E addressable LED controller is the successor to the very popular SP501E controller. Like the SP501E, the SP511E is powered by an ESP8285 with 2MB flash running a firmware for the FairyNest app. Unlike the SP501E, the SP511E comes with an IR receiver and 38 key remote, 3 case push buttons, two output connectors (on same pin), and a microphone. Both the SP501E and SP511E controllers are quite capable, however FairyNest leaves much to be desired. It has 180 dynamic effects, however they are mostly different color combinations of perhaps a dozen animations. And before you can use the app, you have to register with your email.  

To make better use of these controllers, we will be replacing the stock firmware with [WLED](https://github.com/Aircoookie/WLED). WLED is open source and features over 100 animations and 70 color palettes, a large number of interfaces and is very configurable. It won't however be able to take advantage of the microphone. In a later instalment, we will look at installing the Sound Reactive fork of WLED.

#### Setup
Getting set up for the first time can take some time.  But once you have flashed to WLED the first time, you will be able to perform over the air (OTA) updates.  Here is what you will need:
- USB to TTL UART adapter. I'm using the CP2102 available from Amazon or AliExpress.
- Install the CP2102 drivers.
- A program to write to the ESP8266. Review the guide on installing the WLED binary. I will be using esptool in this guide but ESP Home Flasher will work also.
- A clip to attach the CP2102 to the RS232 pads on the bottom of the board, and Dupont wires to attach the clip to the CP2102 adapter. You can purchase pogo pin clips designed for this (2.0mm single row 5 pin). We will be making our own later in this guide.
- The WLED 0.13.0-b2 binary.

#### Building a Clip
If you plan on flashing many of these controllers, I highly recommend purchasing the pogo pin clip. But if you are flashing one or two, it doesn't make sense to pay $11 for a clip to program an $8 controller. I used the long pinned male-female header. The long pins are springy enough to maintain good contact while you program the board.  If you have any Wemos D1 mini boards, you likely have plenty of these laying around. You can purchase them here. The pins have a 2.54mm spacing and the pads are spaced 2.0mm so you will need to bend the pins in a bit. If you have a jumper laying around, put it on pins 4 and 5 before bending. Otherwise solder a piece of wire between pins 4 and 5 after bending. I also bent two outer pins down so they clip on the edge of the board. This isn't required but it allows you to hold the clip firmly in place with one finger. If your header has additional pins, you can cut them off or bend them out of the way. If you don't have a clip and don't want to make one, you can also solder wires to the pads and desolder them once you are done. If you do this, do not solder a Dupont pin on to the pad. Cut and strip the wire and solder the wire to the pad. The rigid pins can rip the pads off of the PCB and you will be stuck with whatever firmware is on the board.

#### Connecting
The pads on board are clearly labelled. When connecting the CP2102 to the clip, connect 3v3 to 3v3 and ground to ground, but cross TX to RX and RX to TX. You also need to connect io0 to ground in order to program it. The CP2102 also has a 5v pin, be sure to use 3v3 and not 5v!
 
#### Programming
Now we are ready to program the board. If esptool detects multiple ports, it can take a while as it attempts to figure out which one to write to. We'll start by figuring out what port our CP2102 is on. Plug the CP2102 in to your USB port then open Device Manager. Expand the "Ports (COM & LPT)" section and note the port for the Silicone Labs CP210x device. Mine happens to be COM4. Now open a Power Shell or CMD window and change directory to where you downloaded the WLED firmware to and type in the following command. If you have the pogo clip and it is attached you can hit enter right away. But if you are using the long-pin headers that need held in place, type the command but do not hit enter. Be sure to replace COM4 with whatever your port is.
`esptool.py -p COM4 write_flash 0x0 SP511E.bin`
Remove the CP2102 from your USB port. Hold the clip in place on the pads with one hand and reinsert the CP2102 into your USB port with the other then hit enter. It will take about 60 seconds to write and verify the firmware. Once it completes and you get the success message you can disconnect the clip and remove the USB adapter.

#### Finishing Up
Connect the controller to a 5-24v power supply and verify you see the WLED-AP wifi access point. If you see it, it succeeded and you can stuff it back in its enclosure and follow the [getting-started guide](https://kno.wled.ge/basics/getting-started/) to get it connected to your network and configured.
