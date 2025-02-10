import serial
import time

class MAX3232:
    def __init__(self, port='/dev/ttyAMA0', baudrate=9600, timeout=1):
        try:
            print(f"Attempting to open serial port {port}")
            # Use the exact same configuration as max3232-test.py
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

    def send_hex(self, hex_string):
        """Send raw hex data. hex_string should be space-separated hex values."""
        if self.ser:
            try:
                # Convert hex string to bytes
                hex_bytes = bytes.fromhex(hex_string.replace(" ", ""))
                print(f"Sending hex: {' '.join(f'{b:02X}' for b in hex_bytes)}")
                
                # Send the bytes directly like in max3232-test.py
                self.ser.write(hex_bytes)
                print(f"Sent {len(hex_bytes)} bytes")
                
                # Small delay to ensure transmission
                time.sleep(0.1)
            except Exception as e:
                print(f"Error sending data: {e}")

    def send(self, data):
        """Send raw string data with CR/LF like max3232-test.py"""
        if self.ser:
            try:
                # Add CR/LF like in max3232-test.py
                message = data + "\r\n"
                self.ser.write(message.encode())
                print(f"Sent: {message.strip()}")
                time.sleep(0.1)
            except Exception as e:
                print(f"Error sending data: {e}")

    def read(self):
        """Read response using the approach from max3232-test.py"""
        if self.ser:
            try:
                if self.ser.in_waiting:
                    received = self.ser.readline().decode(errors='ignore').strip()
                    print(f"Received: {received}")
                    return received
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