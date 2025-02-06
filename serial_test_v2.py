import serial
import time

def test_serial_communication():
    # Configure serial port similar to your working USB-serial test
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
    
    try:
        print(f"Port opened: {ser.name}")
        print("Port settings:", ser.get_settings())
        
        # Test 1: Simple string without protocol formatting
        print("\nTest 1: Simple string")
        test_str = b"Testing 123\r\n"
        print(f"Sending: {test_str}")
        ser.write(test_str)
        time.sleep(1)
        
        # Test 2: OE10 status command without line endings
        print("\nTest 2: OE10 status command (no line ending)")
        command = b"<FF:01:03:ST::7E:G>"
        print(f"Sending: {command}")
        ser.write(command)
        time.sleep(1)
        
        # Test 3: OE10 status command with line endings
        print("\nTest 3: OE10 status command (with line ending)")
        command_with_ending = b"<FF:01:03:ST::7E:G>\r\n"
        print(f"Sending: {command_with_ending}")
        ser.write(command_with_ending)
        time.sleep(1)
        
        # Check for any responses
        while True:
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print("\nReceived:")
                print(f"  Hex: {response.hex()}")
                print(f"  ASCII: {response}")
                print(f"  Bytes: {list(response)}")
            else:
                break
            time.sleep(0.1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        
    finally:
        ser.close()
        print("\nPort closed")

if __name__ == "__main__":
    test_serial_communication() 