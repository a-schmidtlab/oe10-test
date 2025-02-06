import serial
import time

def test_serial_connection(ports=['/dev/ttyAMA0', '/dev/ttyAMA10', '/dev/ttyUSB0'], baudrate=9600):
    for port in ports:
        try:
            print(f"\nTrying port {port}...")
            # Try to open the serial port
            ser = serial.Serial(port, baudrate, timeout=1)
            print(f"✓ Successfully opened {port} at {baudrate} baud")
            
            # Test if we can write and read
            test_message = b"TEST\n"
            ser.write(test_message)
            time.sleep(0.1)
            
            response = ser.read_all()
            print(f"Sent: {test_message}")
            print(f"Received: {response}")
            
            ser.close()
            print("✓ Serial port closed successfully")
            return port
            
        except serial.SerialException as e:
            print(f"✗ Error on {port}: {str(e)}")
    
    print("\nNo working ports found. Troubleshooting tips:")
    print("1. Check if the device is connected properly")
    print("2. Verify the correct port name from the working max3232-test.py")
    print("3. Ensure you have permissions (try 'sudo chmod 666 /dev/ttyAMA0')")
    return None

if __name__ == "__main__":
    working_port = test_serial_connection()
    if working_port:
        print(f"\nSuccess! Working port is: {working_port}") 