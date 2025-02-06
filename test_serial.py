import serial
import time

def test_serial():
    # Open serial port with explicit settings
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1,  # 1 second timeout
        rtscts=False,  # Try with hardware flow control off
        dsrdtr=False   # Try with hardware flow control off
    )
    
    try:
        print(f"Serial port opened: {ser.name}")
        print(f"Current settings: {ser.get_settings()}")
        
        # Set RTS/DTR lines (might help with power)
        ser.setRTS(True)
        ser.setDTR(True)
        time.sleep(0.1)  # Give time for lines to settle
        
        # Test command (Status request) - removed \r\n as it might not be needed
        test_command = b"<FF:01:03:ST::7E:G>"
        print(f"\nSending test command (hex): {test_command.hex()}")
        
        # Send command
        ser.write(test_command)
        time.sleep(0.5)  # Wait for response
        
        # Read response with explicit byte count
        response = ser.read(10)  # Try to read up to 10 bytes
        if response:
            print(f"Received response (hex): {response.hex()}")
            print(f"Received response (ascii): {response}")
        else:
            print("No response received in first read")
        
        # Try reading any remaining data
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print(f"Additional data (hex): {response.hex()}")
            
    finally:
        # Reset lines before closing
        ser.setRTS(False)
        ser.setDTR(False)
        ser.close()
        print("\nSerial port closed")

if __name__ == "__main__":
    test_serial() 