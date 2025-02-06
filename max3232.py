import serial
import time

class MAX3232:
    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=1):
        # Initialize the serial port connection
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            print(f"Connected to MAX3232 on {port} at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error initializing serial connection: {e}")
            self.ser = None

    def send(self, data):
        if self.ser:
            # Encode the string to bytes and send it
            self.ser.write(data.encode())
            time.sleep(0.1)  # delay for data to be sent

    def read(self):
        if self.ser:
            # Read available data from serial
            response = self.ser.read_all().decode(errors='ignore')
            return response
        return ""

    def close(self):
        if self.ser:
            self.ser.close()

# For testing purpose, you can run this module directly.
if __name__ == '__main__':
    max_device = MAX3232()
    max_device.send("Test Command")
    response = max_device.read()
    print("Response:", response)
    max_device.close() 