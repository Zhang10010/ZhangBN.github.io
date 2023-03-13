# Arduino Nano RP2040 Code
These codes need to run on RP2040.   
* The main code that controls the LEGO leg wirelessly is lego_leg.py. It also updates angles to [Adafruit IO](https://io.adafruit.com/ZhangBN/dashboards/lego-leg)
* secrets.py contains wifi connection info   
* mqtt_CBR.py is used to connect to wifi   
* valueMath.py makes it easy to do math with list because micropython doesn't have numpy
* Folder umqtt contains simple.py and robust.py. They are used to connect to adafruit.io   
