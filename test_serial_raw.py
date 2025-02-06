import serial
import time
import binascii

def hex_dump(data):
    """Convert data to hex for debugging"""
    return binascii.hexlify(data).decode()

def test_serial_raw():
    try:
        # Open serial port with explicit settings
        ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
            xonxoff=False,     # Disable software flow control
            rtscts=False,      # Disable hardware flow control
            dsrdtr=False       # Disable hardware flow control
        )
        
        print(f"Port opened: {ser.name}")
        print(f"Port settings:")
        print(f"  Baudrate: {ser.baudrate}")
        print(f"  Bytesize: {ser.bytesize}")
        print(f"  Parity: {ser.parity}")
        print(f"  Stopbits: {ser.stopbits}")
        print(f"  Flow control: {'None'}")
        
        # Clear any pending data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Test 1: Status Command in Hex
        print("\nTest 1: Status Command (Hex)")
        # <FF:01:03:ST::7E:G> in hex
        test_data = bytes.fromhex('3C FF 01 03 53 54 3A 3A 7E 47 3E')
        print(f"Sending: {test_data!r}")
        print(f"Hex: {hex_dump(test_data)}")
        ser.write(test_data)
        time.sleep(0.5)  # Longer wait
        response = ser.read_all()
        print(f"Received: {response!r}")
        print(f"Hex: {hex_dump(response) if response else 'none'}")
        
        # Test 2: Pan Command in Hex
        print("\nTest 2: Pan Command (Hex)")
        # <FF:01:06:PP:000:04:G> in hex
        test_data = bytes.fromhex('3C FF 01 06 50 50 3A 30 30 30 3A 30 34 3A 47 3E')
        print(f"Sending: {test_data!r}")
        print(f"Hex: {hex_dump(test_data)}")
        ser.write(test_data)
        time.sleep(0.5)  # Longer wait
        response = ser.read_all()
        print(f"Received: {response!r}")
        print(f"Hex: {hex_dump(response) if response else 'none'}")
        
        # Test 3: Direct Motor Command
        print("\nTest 3: Direct Motor Command")
        # Try a simple motor command
        test_data = bytes.fromhex('3C FF 01 03 50 4C 3A 3A 7D 47 3E')  # PL (Pan Left) command
        print(f"Sending: {test_data!r}")
        print(f"Hex: {hex_dump(test_data)}")
        ser.write(test_data)
        time.sleep(1.0)  # Even longer wait
        response = ser.read_all()
        print(f"Received: {response!r}")
        print(f"Hex: {hex_dump(response) if response else 'none'}")
        
        # Stop the motor
        time.sleep(2.0)
        stop_data = bytes.fromhex('3C FF 01 03 50 53 3A 3A 7C 47 3E')  # PS (Pan Stop) command
        ser.write(stop_data)
        
        ser.close()
        print("\nPort closed")
        
    except serial.SerialException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_serial_raw() 