= Beer Temperature Logger =

Arduino Uno based temperature logger using a LM35 sensor. The temperature is logged every 10 minutes and added to the log file.

Made for my own usage, probably won't be so useful to anyone else.

== Leds meaning ==
  * Blue : below min temperature (17.5°C)
  * Red : over max temperature (22.5°C)
  * Green : temperature's ok

== What's needed ==
  * Arduino Uno & components
  * Python (I use 2.7 but using it with 3> should be trivial)

== How to use ==
  1. Connect the arduino to your desktop or laptop
  2. Use the arduino tool to compile TemSensor.c and send it to the arduino
  3. Run Logger.py

== Schematic ==

