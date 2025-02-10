import serial
import time

class MAX3232:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, timeout=1):
        try:
            print(f"Attempting to open serial port {port}")
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=timeout
            )
            print(f"Successfully opened {port}")
        except serial.SerialException as e:
            print(f"Error initializing serial connection: {e}")
            self.ser = None

    def send_hex(self, command_string):
        """Send raw hex data. command_string should be a formatted protocol string."""
        if self.ser:
            try:
                # Convert protocol string to actual bytes
                # Example input: "<FF:01:03:ST::7E:G>"
                # Remove < > brackets and convert to bytes
                command_bytes = bytearray()
                
                # Add start bracket
                command_bytes.append(0x3C)  # '<'
                
                # Process the middle part
                parts = command_string.strip('<>').split(':')
                for i, part in enumerate(parts):
                    if i > 0:  # Add separator except for first part
                        command_bytes.append(0x3A)  # ':'
                    
                    # Convert hex values
                    if len(part) == 2 and all(c in '0123456789ABCDEF' for c in part.upper()):
                        command_bytes.append(int(part, 16))
                    else:
                        # Add ASCII characters
                        command_bytes.extend(part.encode())
                
                # Add end bracket
                command_bytes.append(0x3E)  # '>'
                
                print(f"Sending bytes: {' '.join(f'{b:02X}' for b in command_bytes)}")
                self.ser.write(command_bytes)
                print(f"Sent {len(command_bytes)} bytes")
                
                # Small delay to ensure transmission
                time.sleep(0.1)
            except Exception as e:
                print(f"Error sending data: {e}")

    def send(self, data):
        """Send raw string data with CR/LF"""
        if self.ser:
            try:
                message = data + "\r\n"
                self.ser.write(message.encode())
                print(f"Sent: {message.strip()}")
                time.sleep(0.1)
            except Exception as e:
                print(f"Error sending data: {e}")

    def read(self):
        """Read response"""
        if self.ser:
            try:
                if self.ser.in_waiting:
                    # Read until '>' is found or timeout
                    response = bytearray()
                    start_time = time.time()
                    
                    while (time.time() - start_time) < self.ser.timeout:
                        if self.ser.in_waiting:
                            byte = self.ser.read()
                            response.extend(byte)
                            if byte == b'>':  # End of message
                                break
                    
                    if response:
                        try:
                            # Try to decode as ASCII first
                            decoded = response.decode(errors='ignore')
                            print(f"Received: {decoded}")
                            return decoded
                        except UnicodeDecodeError:
                            # If ASCII decode fails, return hex representation
                            hex_str = ' '.join(f'{b:02X}' for b in response)
                            print(f"Received hex: {hex_str}")
                            return hex_str
                return ""
            except Exception as e:
                print(f"Error reading data: {e}")
        return ""

    def close(self):
        """Close the serial port"""
        if self.ser:
            try:
                self.ser.close()
                print("Serial port closed")
            except Exception as e:
                print(f"Error closing port: {e}")

if __name__ == '__main__':
    import serial.tools.list_ports
    
    # List all available serial ports
    print("Available serial ports:")
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        print(f"- {port.device}: {port.description}")
    
    # Test connection
    port = input("Enter port to test (e.g., /dev/ttyAMA0): ")
    max_device = MAX3232(port=port)
    
    if max_device.ser:
        try:
            while True:
                # Test with status command
                print("\nSending status command...")
                status_command = "3C FF 3A 01 3A 03 3A 53 54 3A 3A 7E 3A 47 3E"
                max_device.send_hex(status_command)
                response = max_device.read()
                if response:
                    print(f"Response: {response}")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nTest terminated by user")
        finally:
            max_device.close() 