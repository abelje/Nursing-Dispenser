# Nursing Dispenser
## Introduction
This project is made as an independent research project into creating an interface to allow the WLC Nursing Department to be able to fake dispensing drugs similar to a hospital. There are two parts for this project, the hardware, setting up the Raspberry Pi and 3d printing components. The other is the frontend, building the GUI and creating the necessary database.

## Raspberry Pi Hardware Setup
For this project, we made use of a Raspberry Pi 3. These instructions are built assuming you are using a raspberry pi.

Solder on any neccessary pins for the raspberry pi.

### Installing the OS
Information for installing Raspberry Pi OS can be found [here](https://www.raspberrypi.com/software/). Download the Raspberry Pi imager and set up the sd card using your computer.

### GPIO Pinout
Raspberry Pi pinouts can be found on this website: (https://pinout.xyz/)[https://pinout.xyz/]

### Raspberry Pi Environment Setup
The library gpiozero can be used to interface with raspberry pi pins in python. Information about it can be found here: [https://gpiozero.readthedocs.io/en/stable/installing.html](https://gpiozero.readthedocs.io/en/stable/installing.html)

#### Pigpio
Pigpio is required to stop jitter of servos on the raspberry pi. Make it a startup program by following these instructions.

1. Build pigpio daemon from the github repository (it is not in the apt repository for whatever reason):

    ```
    git clone https://github.com/joan2937/pigpio
    cd pigpio
    make
    sudo make install
    sudo ldconfig
    ```
2. Test run pigpio using ```sudo pigpiod```

3. Continue to make it a startup program.

4. Create a new system service using ```sudo nano /etc/systemd/system/pigpiod.service``` and paste the following:

    ```
    [Unit]
    Description=Daemon required to control GPIO pins via pigpio
    After=network.target

    [Service]
    Type=forking
    ExecStart=/usr/local/bin/pigpiod -l
    ExecStop=/bin/systemctl kill pigpiod
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
2. Enable the service for startups: ```sudo systemctl enable pigpiod```

### Create Desktop Shortcut for Python Script
1. Add ```#!/usr/bin/env python3``` to the top of the script being used.
2. Create an executable using ```chmod +x /path/script.py```
3. Create text file on desktop, naming it with the ```.desktop``` filetype.
4. Open the file in a text editor and edit the config in this style:

    ```
    [Desktop Entry]
    Name=program.desktop
    Exec=env/bin/python3 /path/p.py
    Icon=/path/icon.png
    Type=Application
    Categories=Programming
    Terminal=false
    ```

### Adafruit Hat
For this project, we required more than the standard 2 or 3 PWM pins on a Raspberry Pi. We can extend this with a hat, which is found below.

16 Channel PWM Hat: [https://www.adafruit.com/product/2327](https://www.adafruit.com/product/2327)

The hat we got requires a circuit python library to work. Blinka needs to be installed to serve as a interface layer for the Raspberry Pi. You will also have to solder on the pins which is covered in the setup documentation.

#### Installing Blinka
Installation documentation: [https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)

1. Follow the tutorial linked above

2. It will prompt a Reboot

#### Installing the necessary library
Adafruit documentation for using the library: [https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library] (https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library)

1. Activate the virtual environment: ```source env/bin/activate```
2. Install the library to interface with the hat using ```pip3 install adafruit-circuitpython-servokit```
3. The virtual environment is required to be activated before running a python script with the Servo Hat.
4. NOTE: The virtual environment can be activated in the shortcut, see the shortcut section for more details. The implementation of this library can be found in ```hardware/drawer.py```.

### 3D Print Files
Files are located under ```hardware/3D-Models```. The Raspberry Pi case files original creators are linked below. We extended the top case further in Tinkercad. This file is ```Extended-PI3-Cap.stl``` which allows enough room for the hat and extra wires.

#### Credits
- VESA_TOP_hexagon_expanded.stl from [Extended PI Case](https://www.printables.com/model/1118535-pi-3-b-case-with-space-for-hats/files) by Rafael Passos on Printables
- VESA_BASE_75.stl from [Raspberry PI 3 B+ Case](https://www.printables.com/model/195683-raspberry-pi-3-b-case/files) by Alex A. on Printables
- Power Supply Box by Jonathan Abel [Tinkercad Power Supply Box](https://www.tinkercad.com/things/j4cFT0lMdoc-box-for-power-supply?sharecode=JTmyIY8HDY2GwD2qaHnmSiif7J7ZKLIcgQRIuaZ3pcA)
- Drawer Files Supplied by Professor