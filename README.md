# OE10 Remote Control Project

## Overview

This project implements a web-based remote control interface for the OE10 pan and tilt unit. The system uses a Raspberry Pi 5 running Debian as the controller, connected to the OE10 via an ARCELI MAX3232 serial adapter.

## Features

- Web-based control interface
- Real-time pan and tilt control
- Status monitoring
- Debug information display
- Responsive design
- Error handling and user feedback

## Hardware Requirements

- Raspberry Pi 5 (running Debian)
- ARCELI MAX3232 serial adapter
- OE10 pan and tilt unit

## Software Requirements

- Python 3.x
- Flask
- PySerial

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd oe10-project
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```bash
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://<raspberry-pi-ip>:5000
   ```

3. Use the web interface to:
   - Control pan and tilt angles
   - Monitor device status
   - View debug information

## Project Structure

- `app.py`: Flask server that serves the web interface and communicates with the OE10 via the OE10 protocol module.
- `max3232.py`: Module that handles serial communication with the MAX3232 adapter.
- `oe10_protocol.py`: Contains methods to communicate with the OE10 unit using its protocol.
- `templates/index.html`: The web interface where users send control commands to the OE10 unit.

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


## Debug Information

The web interface displays detailed debug information regarding the communications with the OE10, including the current status of the unit and the low-level command logs.

## Troubleshooting

### No Response from OE10 Unit
If commands are being sent but no responses are received:

1. Check Physical Connections
   - Verify all cables are securely connected
   - Ensure the MAX3232 adapter is properly powered
   - Check TX/RX wire connections are not reversed
   - Verify ground connection is solid

2. Serial Port Configuration
   - Confirm baud rate matches OE10 specifications (typically 9600)
   - Verify serial port settings:
     ```bash
     stty -F /dev/ttyUSB0 -a  # Replace with your port
     ```
   - Default settings should be:
     - 9600 baud
     - 8 data bits
     - 1 stop bit
     - No parity
     - No flow control

3. Signal Verification
   - Use a multimeter to check voltage levels:
     - RS-232 signals should swing between +/-3V to +/-15V
     - TTL signals should be 0V/3.3V or 0V/5V
   - Monitor TX/RX LED indicators on the MAX3232 adapter if available

4. Software Checks
   - Run with elevated permissions: `sudo python app.py`
   - Verify correct serial port is selected
   - Try different serial port timeouts
   - Enable debug logging in PySerial:
     ```python
     import logging
     logging.basicConfig(level=logging.DEBUG)
     logging.getLogger('serial').setLevel(logging.DEBUG)
     ```

### Testing Serial Communication
Use the following command to test basic serial port functionality:
```bash
echo "test" > /dev/ttyUSB0  # Replace with your port
```

For a loopback test, connect TX to RX and run:
```bash
python3 -m serial.tools.miniterm /dev/ttyUSB0 9600
```