# IA_KNearest_Hydrometer_Reader
Python and c++ code running on an arduino uno connected to an esp32-cam, using artificial intelligence to recognize the digits.

Intructions for the use:

1 step (Setting Up):

|ARDUINO UNO|

Connect the ESP32-Cam pins in to the Arduino Uno following the part 1 of image01:

Rasp |-----| Uno                Rasp |-----| Rasp                Uno |-----| Uno
5v          5v                  gnd         IO0                  Reset      gnd
gnd         gnd
VoT         Digital01(TX)
Vor         Digital02(RX)

|FTDI|

Rasp |-----|FTDI                Rasp |-----| Rasp
5v          Vcc                  gnd         IO0
gnd         gnd
VoT         TX
Vor         RX

2 step (Arduino Rasp):

Set tools preferences:
Board: "ESP32 Wrover Module"
Upload Speed: "115200"
Flash Frequency: "40MHz"
Partition Scheme: "Huge APP (3MB No OTA/1MB SPIFFS)"
Core Debug Level: "Nothing"
Porta: "Your COM with Arduino Uno"

Compile and Upload the CameraWeServer.ino
When you see "Connecting........_____....._____....." hit the little button in the back of ESP32-Cam
Let it write 100%
When prints "Leaving...
Hard resetting via RTS pin..."
Remove the IO0 to gnd cable
Open the Monitor Serial
And Hit the little button again.
Copy the IP

3 step (Python Usage):
Open Arduino_Stream.py and paste the IP
Run the HidroReader
