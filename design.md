## Objective of this test implementation is to control the OE10 remotely via a web interface.

OE10 is a serial pan and tilt unit. It is connected via a serial adapter ARCELI MAX3232 to a Raspberry Pi 5 (debiaian). 
max3232-test.py is a sample code how to handle the MAX3232
The web interface is a simple html page that allows the user to control the OE10 from a remotely connected web browser.
The Raspberry Pi uses the communication protocol defined in the OE10_Protocoll.md file to communicate with the OE10.
The web interface is served by the Raspberry Pi.
The web interfaces allows all features defined in the OE10_Protocoll.md file and shows the current status of the OE10 and detailed debug information.
the test uses venv to create a virtual python environment and install the dependencies.

oe10-project/
├── app.py                    # Main Flask server
├── oe10_protocol.py          # Handling communication protocol for OE10
├── max3232.py               # Code to handle the MAX3232 serial adapter (adapted from max3232-test.py)
├── static/
│   └── styles.css           # (Optional) Basic styling for web interface
├── templates/
│   └── index.html           # Web interface HTML page
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies
