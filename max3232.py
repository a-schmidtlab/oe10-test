import serial
import time

class MAX3232:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, timeout=1):
        # Initialize the serial port connection
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=timeout,
                xonxoff=False,
                rtscts=False
            )
            # Clear any existing data
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            print(f"Connected to MAX3232 on {port} at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error initializing serial connection: {e}")
            self.ser = None

    def send_hex(self, hex_string):
        """Send raw hex data. hex_string should be space-separated hex values."""
        if self.ser:
            try:
                # Convert hex string to bytes
                hex_bytes = bytes.fromhex(hex_string)
                print(f"Sending hex: {' '.join(f'{b:02X}' for b in hex_bytes)}")
                
                # Clear input buffer before sending
                self.ser.reset_input_buffer()
                # Send the bytes
                self.ser.write(hex_bytes)
                self.ser.flush()  # Wait until all data is written
                time.sleep(0.2)  # Delay for data to be sent and processed
            except serial.SerialException as e:
                print(f"Error sending data: {e}")
            except ValueError as e:
                print(f"Error converting hex string: {e}")

    def send(self, data):
        """Convert ASCII command to hex and send"""
        if self.ser:
            try:
                # Convert ASCII to hex bytes
                hex_bytes = data.encode()
                print(f"Sending ASCII as hex: {' '.join(f'{b:02X}' for b in hex_bytes)}")
                
                # Clear input buffer before sending
                self.ser.reset_input_buffer()
                # Send the bytes
                self.ser.write(hex_bytes)
                self.ser.flush()  # Wait until all data is written
                time.sleep(0.2)  # Delay for data to be sent and processed
            except serial.SerialException as e:
                print(f"Error sending data: {e}")

    def read(self):
        if self.ser:
            try:
                # Wait a bit for the response to arrive
                time.sleep(0.1)
                
                # Read data with timeout
                response = b""
                start_time = time.time()
                
                while (time.time() - start_time) < self.ser.timeout:
                    if self.ser.in_waiting:
                        new_data = self.ser.read(self.ser.in_waiting)
                        if new_data:
                            response += new_data
                            print(f"Received hex: {' '.join(f'{b:02X}' for b in new_data)}")
                        else:
                            break
                    time.sleep(0.05)
                
                return response.decode(errors='ignore')
            except serial.SerialException as e:
                print(f"Error reading data: {e}")
        return ""

    def close(self):
        if self.ser:
            try:
                self.ser.close()
            except serial.SerialException as e:
                print(f"Error closing port: {e}")

# For testing purpose, you can run this module directly.
if __name__ == '__main__':
    max_device = MAX3232()
    
    # Test with the known working command
    working_command = "3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E"
    print("\nTesting with known working command...")
    max_device.send_hex(working_command)
    response = max_device.read()
    print(f"Response: {response!r}")
    
    # Test status command in hex
    status_command = "3C FF 3A 01 3A 03 3A 53 54 3A 3A 7E 3A 47 3E"
    print("\nTesting status command...")
    max_device.send_hex(status_command)
    response = max_device.read()
    print(f"Response: {response!r}")
    
    max_device.close() 