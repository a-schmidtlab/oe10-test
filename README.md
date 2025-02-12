# OE10 Pan/Tilt Control Interface

A web-based control interface for the OE10-104 Serial Pan and Tilt Unit. This application provides a user-friendly way to control and monitor the OE10 device through a web browser.

## Features

- Real-time pan and tilt control
- Absolute position movement
- Proportional speed control
- Status monitoring
- Protocol and software version information
- Clean and responsive web interface

## Hardware Requirements

- Raspberry Pi (tested on Pi 5)
- ARCELI MAX3232 serial adapter
- OE10-104 Pan/Tilt Unit
- Power supply for OE10

## Hardware Setup

1. Connect the ARCELI MAX3232 module to the Raspberry Pi:
   - Connect MAX3232's TTL-level RX to Pi's TX (GPIO14)
   - Connect MAX3232's TTL-level TX to Pi's RX (GPIO15)
   - Connect GND between Pi and MAX3232
   - Power MAX3232 with 3.3V or 5V from Pi

2. Connect the MAX3232 to the OE10:
   - Connect MAX3232's RS232 RX to OE10's TX
   - Connect MAX3232's RS232 TX to OE10's RX
   - Connect GND between MAX3232 and OE10

## Software Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/oe10-control.git
   cd oe10-control
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Enable UART on Raspberry Pi:
   ```bash
   sudo raspi-config
   # Navigate to Interface Options > Serial Port
   # Disable serial login shell
   # Enable serial interface
   ```

## Configuration

The default configuration uses `/dev/ttyAMA0` for serial communication. If you need to change this:

1. Open `oe10_protocol.py`
2. Modify the default port in the `OE10Protocol` class initialization:
   ```python
   def __init__(self, port='/dev/ttyAMA0', baudrate=9600):
   ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Access the web interface:
   - Open a web browser
   - Navigate to `http://your_raspberry_pi_ip:5000`

3. Control Interface Features:
   - Use arrow buttons for directional control
   - Enter specific angles for absolute positioning
   - Monitor current position and status
   - View protocol and software versions

## API Endpoints

- `GET /api/status` - Get current device status
- `POST /api/move` - Move to absolute position
- `POST /api/proportional` - Proportional movement control
- `POST /api/stop` - Stop all movement
- `GET /api/versions` - Get protocol and software versions

## Protocol Implementation

The application implements the OE10-104 communication protocol as specified in the protocol documentation. Key features include:

- Packet structure: `<to:from:length:command:data:checksum:checksum ind>`
- XOR checksum calculation
- ACK/NAK handling
- Error detection and reporting

## Troubleshooting

1. Serial Connection Issues:
   - Verify UART is enabled on Raspberry Pi
   - Check physical connections
   - Verify serial port permissions
   - Check baud rate settings

2. Movement Issues:
   - Verify power supply to OE10
   - Check status response for errors
   - Verify command format in protocol

3. Web Interface Issues:
   - Check Flask server is running
   - Verify network connectivity
   - Check browser console for errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

[Your chosen license]

## Acknowledgments

- OE10-104 Protocol Documentation
- Flask Web Framework
- Bootstrap for UI components