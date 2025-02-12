import serial
import time

class OE10Protocol:
    """Implementation of the OE10-104 Serial Pan and Tilt Unit protocol"""
    
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600):
        """Initialize with exact settings from working configuration"""
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        
        # Use addresses from working captures
        self.CONTROLLER_ID = 0x01
        self.PERIPHERAL_ID = 0x03  # Changed from 0x02 to 0x03
        self.BROADCAST_ID = 0xFF
        
        # Constants
        self.ACK = 0x06  # ASCII ACK character
        self.NAK = 0x15  # ASCII NAK character
        
        # Current state
        self.current_pan = 0
        self.current_tilt = 0

        # Add status caching
        self._last_status = None
        self._last_status_time = 0
        self._status_cache_duration = 2  # seconds

    def _calculate_checksum(self, data):
        """Calculate XOR checksum of packet data
        
        Args:
            data (str): Packet data excluding < and checksum section
            
        Returns:
            tuple: (checksum byte, checksum indicator)
        """
        checksum = 0
        for byte in data.encode('ascii'):
            checksum ^= byte
            
        # Handle special cases as per protocol
        if checksum == 0x3C:  # '<'
            return 'FF', '0'
        elif checksum == 0x3E:  # '>'
            return 'FF', '1'
        else:
            return format(checksum, '02X'), 'G'

    def _build_packet(self, command, data=""):
        """Build packet exactly as seen in hexdump
        Examples from dump:
        Status (ST):  3c 03 3a 01 3a 03 3a 53 54 3a 3a 06 3a 47 3e
        AS check:     3c 03 3a 01 3a 03 3a 41 53 3a 3a 13 3a 47 3e
        PC command:   3c 03 3a 01 3a 07 3a 50 43 3a [data] 3a [checksum] 3a 47 3e
        """
        to_addr = "03"
        from_addr = "01"
        
        # Fixed lengths from hexdump
        if command == "PC":
            length = "07"
        else:
            length = "03"
        
        # Fixed checksums from hexdump
        checksums = {
            "ST": "06",
            "AS": "13",
            "PC": None  # Will be added with data
        }
        
        packet = f"<{to_addr}:{from_addr}:{length}:{command}:"
        if data:
            packet += f"{data}:"
        else:
            packet += ":"
        
        # Add appropriate checksum
        if command in checksums and checksums[command]:
            packet += f"{checksums[command]}:"
        
        packet += "G>"
        return packet

    def _send_command(self, command, data=""):
        """Send command with exact timing from hexdump"""
        # Every command is preceded by AS status check
        self._send_status_check()
        
        # Send command (some commands are sent twice in hexdump)
        packet = self._build_packet(command, data)
        print(f"Sending: {packet}")
        self.serial.write(packet.encode('ascii'))
        self.serial.flush()
        
        # Commands are often duplicated in hexdump
        if command in ["ST", "PC"]:
            time.sleep(0.1)
            self.serial.write(packet.encode('ascii'))
            self.serial.flush()
        
        # Wait for response as seen in dump
        time.sleep(0.1)
        response = self.serial.readline().decode('ascii').strip()
        print(f"Response: {response}")
        return response

    def _send_status_check(self):
        """AS status check exactly as seen in hexdump"""
        packet = "<03:01:03:AS::13:G>"
        self.serial.write(packet.encode('ascii'))
        self.serial.flush()
        time.sleep(0.1)
        response = self.serial.readline()
        return response

    def get_status(self):
        """Status command exactly as seen in hexdump"""
        # Send ST command: 3c 03 3a 01 3a 03 3a 53 54 3a 3a 06 3a 47 3e
        response = self._send_command("ST")
        if not response:
            return None
        
        try:
            # Parse response format from hexdump
            # Example: <01:03:0D:06:ST18000150010:13:G>
            parts = response[1:-1].split(':')
            if len(parts) >= 6:
                status_data = parts[4][2:]  # Skip 'ST'
                return {
                    "pan_position": int(status_data[3:6]),
                    "tilt_position": int(status_data[6:9])
                }
        except Exception as e:
            print(f"Error parsing status: {e}")
        return None

    def move_pan_to(self, degrees):
        """Absolute pan movement using PC command as seen in dump"""
        # Convert degrees to proportional command
        if degrees > self.current_pan:
            return self.proportional_control(pan_direction=2, pan_speed=50)
        elif degrees < self.current_pan:
            return self.proportional_control(pan_direction=1, pan_speed=50)
        return True

    def move_tilt_to(self, degrees):
        """Absolute tilt movement using PC command as seen in dump"""
        # Convert degrees to proportional command
        if degrees > self.current_tilt:
            return self.proportional_control(tilt_direction=1, tilt_speed=50)
        elif degrees < self.current_tilt:
            return self.proportional_control(tilt_direction=2, tilt_speed=50)
        return True

    def stop(self):
        """Stop command exactly as seen in hexdump"""
        return self.proportional_control()  # Uses the stop pattern 000000003a16

    def proportional_control(self, pan_direction=0, tilt_direction=0, 
                           pan_speed=0, tilt_speed=0):
        """Movement commands exactly as captured in hexdump"""
        # Exact command patterns from hexdump
        if pan_direction == 1:  # Left
            data = "023200003a26"
        elif pan_direction == 2:  # Right
            data = "013200003a25"
        elif tilt_direction == 1:  # Up
            data = "08001e003a00"
        elif tilt_direction == 2:  # Down
            data = "0400280003a3a"
        else:  # Stop
            data = "000000003a16"
        
        # Send PC command twice as seen in hexdump
        self._send_command("PC", data)
        time.sleep(0.1)
        return self._send_command("PC", data) is not None

    def get_protocol_version(self):
        """Get protocol version
        
        Returns:
            str: Version string or None
        """
        response = self._send_command("PV")
        if response and response['command'] == 'PV':
            return response['data']
        return None

    def get_software_version(self):
        """Get software version
        
        Returns:
            str: Version string or None
        """
        response = self._send_command("CV")
        if response and response['command'] == 'CV':
            version = response['data']
            if len(version) >= 6:
                major = f"{version[0]}{version[1]}"
                minor = f"{version[2]}{version[3]}"
                revision = f"{version[4]}{version[5]}"
                return f"{major}.{minor}.{revision}"
        return None

    def close(self):
        """Close the serial connection and cleanup resources"""
        try:
            if hasattr(self, 'serial') and self.serial and self.serial.is_open:
                self.serial.close()
                print("Serial connection closed successfully")
        except Exception as e:
            print(f"Error closing serial connection: {e}")

if __name__ == "__main__":
    # Basic test
    oe10 = OE10Protocol()
    print("Testing connection...")
    
    # Get status
    status = oe10.get_status()
    print(f"Status: {status}")
    
    # Test movement
    print("Testing pan movement...")
    oe10.move_pan_to(90)
    time.sleep(2)
    oe10.move_pan_to(0)
    
    oe10.close() 