from max3232 import MAX3232
import time

class OE10Controller:
    def __init__(self, port='/dev/ttyAMA0'):
        self.device = MAX3232(port=port)
        self.current_pan = 0
        self.current_tilt = 0
        self.controller_id = 0x01  # Controller ID is always 0x01
        self.peripheral_id = 0x02  # Default peripheral ID
        self.broadcast_id = 0xFF   # Broadcast address
        self.ACK = 0x06  # ASCII ACK character
        self.NAK = 0x15  # ASCII NAK character

    def _calculate_checksum(self, data):
        """Calculate XOR checksum of all bytes in data (excluding < and checksum section)"""
        checksum = 0
        for byte in data:
            checksum ^= ord(byte)
        
        # Handle special cases as per protocol
        if checksum == 0x3C:  # '<'
            return 'FF', '0'
        elif checksum == 0x3E:  # '>'
            return 'FF', '1'
        else:
            return format(checksum, '02X'), 'G'

    def _format_command(self, command, data=""):
        """Format a command according to protocol
        <to:from:length:command:data:checksum:checksum ind>
        """
        to_addr = format(self.peripheral_id, '02X')
        from_addr = format(self.controller_id, '02X')
        
        # Calculate length: command + data + joining colon (if data exists)
        packet_content = f"{command}"
        if data:
            packet_content += f":{data}"
        length = len(packet_content)
        length_str = format(length, '02X')
        
        # Build complete packet content for checksum calculation
        full_content = f"{to_addr}:{from_addr}:{length_str}:{packet_content}"
        checksum, checksum_ind = self._calculate_checksum(full_content)
        
        return f"<{full_content}:{checksum}:{checksum_ind}>"

    def _parse_response(self, response):
        """Parse response from device, handle ACK/NAK"""
        if not response:
            return None
            
        try:
            # Remove < > brackets
            response = response[1:-1]
            parts = response.split(':')
            
            if len(parts) < 4:
                return None
                
            # Check if it's a NAK response
            if parts[3] == chr(self.NAK):
                error_code = int(parts[4], 16) if len(parts) > 4 else 0
                error_msgs = {
                    0x01: "Device under control of another controller",
                    0x08: "Command not available for device",
                    0x10: "Command not recognized",
                    0x20: "Device timed out"
                }
                error = error_msgs.get(error_code, "Unknown error")
                print(f"NAK received: {error}")
                return None
                
            # Handle ACK response
            if parts[3] == chr(self.ACK):
                return parts[4] if len(parts) > 4 else "ACK"
                
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None

    def get_status(self):
        """Get the current status from the OE10 device."""
        command = self._format_command("ST")
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("ST"):
            # Parse status bytes according to protocol
            status_bytes = parsed[2:]
            if len(status_bytes) >= 9:
                features = int(status_bytes[0], 16)
                error_status = int(status_bytes[1], 16)
                pan_pos = status_bytes[3:6]
                tilt_pos = status_bytes[6:9]
                return {
                    "pan_supported": bool(features & 0x08),
                    "tilt_supported": bool(features & 0x10),
                    "error_present": bool(error_status & 0x20),
                    "pan_position": int(pan_pos),
                    "tilt_position": int(tilt_pos)
                }
        return None

    def get_protocol_version(self):
        """Request Protocol Version Command (PV)"""
        command = self._format_command("PV")
        self.device.send_hex(command)
        response = self.device.read()
        return self._parse_response(response)

    def get_software_version(self):
        """Request Software Version Command (CV)"""
        command = self._format_command("CV")
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("CV"):
            version_bytes = parsed[2:]
            if len(version_bytes) >= 6:
                major = f"{version_bytes[0]}{version_bytes[1]}"
                minor = f"{version_bytes[2]}{version_bytes[3]}"
                revision = f"{version_bytes[4]}{version_bytes[5]}"
                return f"{major}.{minor}.{revision}"
        return None

    def change_id(self, new_id):
        """Change ID Command (SI)"""
        if not (0x02 <= new_id <= 0xFE):
            print("Invalid ID. Must be between 0x02 and 0xFE")
            return False
        command = self._format_command("SI", format(new_id, '02X'))
        self.device.send_hex(command)
        response = self.device.read()
        if self._parse_response(response):
            self.peripheral_id = new_id
            return True
        return False

    def move_pan_to(self, degrees):
        """Move pan to specific position in degrees (0-360)"""
        # Ensure degrees is within 0-360 range and convert to integer
        degrees = int(degrees % 360)
        # Format position as 3-digit string
        pos = f"{degrees:03d}"
        command = self._format_command("PP", pos)
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("PP"):
            self.current_pan = degrees
            return True
        return False

    def move_tilt_to(self, degrees):
        """Move tilt to specific position in degrees (-90 to +90)"""
        # Clamp degrees to valid range and convert to integer
        degrees = int(max(-90, min(90, degrees)))
        # Format position as 3-digit string
        pos = f"{abs(degrees):03d}"
        command = self._format_command("TP", pos)
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("TP"):
            self.current_tilt = degrees
            return True
        return False

    def pan_left(self):
        """Pan Left Command (PL)"""
        command = self._format_command("PL")
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("PL"):
            self.current_pan = int(parsed[2:5])
            return True
        return False

    def pan_right(self):
        """Pan Right Command (PR)"""
        command = self._format_command("PR")
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("PR"):
            self.current_pan = int(parsed[2:5])
            return True
        return False

    def pan_stop(self):
        """Pan Stop Command (PS)"""
        command = self._format_command("PS")
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("PS"):
            self.current_pan = int(parsed[2:5])
            return True
        return False

    def tilt_up(self):
        """Tilt Up Command (TU)"""
        command = self._format_command("TU")
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("TU"):
            self.current_tilt = int(parsed[2:5])
            return True
        return False

    def tilt_down(self):
        """Tilt Down Command (TD)"""
        command = self._format_command("TD")
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("TD"):
            self.current_tilt = int(parsed[2:5])
            return True
        return False

    def tilt_stop(self):
        """Tilt Stop Command (TS)"""
        command = self._format_command("TS")
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        if parsed and parsed.startswith("TS"):
            self.current_tilt = int(parsed[2:5])
            return True
        return False

    def proportional_control(self, pan_direction=0, tilt_direction=0, 
                           pan_speed=0, tilt_speed=0):
        """Proportional Control Command (PC)
        pan_direction: 0=Stop, 1=Left, 2=Right
        tilt_direction: 0=Stop, 1=Up, 2=Down
        speed: 0-100 (will be converted to 0x00-0x64)
        """
        # Validate and clamp inputs
        pan_direction = max(0, min(2, pan_direction))
        tilt_direction = max(0, min(2, tilt_direction))
        pan_speed = max(0, min(100, pan_speed))
        tilt_speed = max(0, min(100, tilt_speed))

        # Create command byte
        cmd_byte = (pan_direction & 0x03) | ((tilt_direction & 0x03) << 2)
        
        # Format data
        data = f"{format(cmd_byte, '02X')}{format(pan_speed, '02X')}{format(tilt_speed, '02X')}00"
        
        command = self._format_command("PC", data)
        self.device.send_hex(command)
        return self._parse_response(self.device.read()) is not None

    def proportional_control_feedback(self, pan_direction=0, tilt_direction=0, 
                                   pan_speed=0, tilt_speed=0):
        """Proportional Control with Feedback Command (PF)"""
        # Similar to PC but returns position information
        pan_direction = max(0, min(2, pan_direction))
        tilt_direction = max(0, min(2, tilt_direction))
        pan_speed = max(0, min(100, pan_speed))
        tilt_speed = max(0, min(100, tilt_speed))

        cmd_byte = (pan_direction & 0x03) | ((tilt_direction & 0x03) << 2)
        data = f"{format(cmd_byte, '02X')}{format(pan_speed, '02X')}{format(tilt_speed, '02X')}00"
        
        command = self._format_command("PF", data)
        self.device.send_hex(command)
        response = self.device.read()
        parsed = self._parse_response(response)
        
        if parsed and parsed.startswith("PF"):
            # Parse response according to protocol
            return {
                "pan_speed": int(parsed[2], 16),
                "tilt_speed": int(parsed[3], 16),
                "tilt_position": int(parsed[4:7]),
                "pan_position": int(parsed[7:10]),
                "pan_endstops": parsed[10] == '1',
                "tilt_endstops": parsed[11] == '1'
            }
        return None

    def move(self, pan=None, tilt=None):
        """Move both pan and tilt (if provided)"""
        responses = []
        if pan is not None:
            responses.append(self.move_pan_to(pan))
        if tilt is not None:
            responses.append(self.move_tilt_to(tilt))
        return '; '.join(responses) if responses else "No movement parameters provided"

    def debug_info(self):
        """Get error diagnosis information"""
        command = self._format_command("ED")
        self.device.send(command)
        debug = self.device.read()
        if not debug:
            debug = "No debug information available"
        return debug

    def close_connection(self):
        self.device.close()

if __name__ == "__main__":
    controller = OE10Controller()
    print("Testing pan movement...")
    print("Moving to 0°")
    print(controller.move_pan_to(0))
    time.sleep(2)
    print("Moving to +20°")
    print(controller.move_pan_to(20))
    time.sleep(2)
    print("Moving to -20°")
    print(controller.move_pan_to(340))  # -20° is 340° in 360° system
    controller.close_connection() 