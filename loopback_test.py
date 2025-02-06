import serial
import time

def test_loopback():
    """
    This test requires TX and RX to be connected on the MAX3232 side
    (T1OUT connected to R1IN) for loopback testing
    """
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        timeout=1
    )
    
    try:
        print("Starting loopback test...")
        print("Please connect T1OUT to R1IN on the MAX3232")
        time.sleep(2)  # Give time to make connection if needed
        
        test_data = b"TEST123"
        print(f"\nSending: {test_data}")
        
        ser.write(test_data)
        time.sleep(0.1)
        
        response = ser.read(len(test_data))
        if response:
            print(f"Received: {response}")
            if response == test_data:
                print("SUCCESS: Loopback test passed!")
            else:
                print("FAIL: Data received but doesn't match")
        else:
            print("FAIL: No data received")
            
    finally:
        ser.close()
        print("\nTest completed")

if __name__ == "__main__":
    test_loopback() 