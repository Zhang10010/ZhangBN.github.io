# Arduino Nano RP2040 Code
These codes need to run on RP2040.   
* The main code that controls the LEGO leg wirelessly is lego_leg.py. It also updates angles to [Adafruit IO](https://io.adafruit.com/)
* secrets.py contains wifi connection info    
* valueMath.py makes it easy to do math with list because micropython doesn't have numpy
* Folder umqtt contains simple.py and robust.py. They are used to connect to Adafruit IO  
* mqtt_CBR.py is a library that utilizes simple.py to connect to Wi-Fi and the LEGO leg broker  
