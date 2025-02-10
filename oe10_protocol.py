from max3232 import MAX3232
import time

class OE10Controller:
    def __init__(self, port='/dev/ttyAMA0'):
        self.device = MAX3232(port=port)
        self.current_pan = 0
        self.current_tilt = 0
        self.controller_id = 0x01  # Controller ID is always 0x01
        self.broadcast_id = 0xFF   # Broadcast address

    def _calculate_checksum(self, data):
        """Calculate XOR checksum of all bytes in data"""
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
        """Format a command according to protocol"""
        # Format: <to:from:length:command:data:checksum:checksum_ind>
        to_addr = format(self.broadcast_id, '02X')  # FF for broadcast
        from_addr = format(self.controller_id, '02X')  # 01 for controller
        
        # Calculate length (command + data + separator if data exists)
        length = len(command) + (len(data) + 1 if data else 0)
        length_str = format(length, '02X')
        
        # Build packet content
        packet_content = f"{to_addr}:{from_addr}:{length_str}:{command}"
        if data:
            packet_content += f":{data}"
        
        # Calculate checksum
        checksum, checksum_ind = self._calculate_checksum(packet_content)
        
        # Build final packet
        return f"<{packet_content}:{checksum}:{checksum_ind}>"

    def get_status(self):
        """Get the current status from the OE10 device."""
        command = self._format_command("ST")
        self.device.send(command)
        response = self.device.read()
        return response

    def move_pan_to(self, degrees):
        """Move pan to specific position in degrees (0-360)"""
        # Ensure degrees is within 0-360 range and convert to integer
        degrees = int(degrees % 360)
        # Format position as 3-digit string
        pos = f"{degrees:03d}"
        command = self._format_command("PP", pos)
        self.device.send(command)
        response = self.device.read()
        self.current_pan = degrees
        return response

    def move_tilt_to(self, degrees):
        """Move tilt to specific position in degrees (-90 to +90)"""
        # Clamp degrees to valid range and convert to integer
        degrees = int(max(-90, min(90, degrees)))
        # Format position as 3-digit string
        pos = f"{abs(degrees):03d}"
        command = self._format_command("TP", pos)
        self.device.send(command)
        response = self.device.read()
        self.current_tilt = degrees
        return response

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