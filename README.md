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

## Debug Information

The web interface displays detailed debug information regarding the communications with the OE10, including the current status of the unit and the low-level command logs.