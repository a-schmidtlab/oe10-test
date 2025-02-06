import serial
import time

def test_direct_loopback():
    """
    For this test, temporarily connect:
    GPIO14 (TX) directly to GPIO15 (RX) on the Raspberry Pi
    """
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        timeout=1
    )
    
    try:
        print("Testing direct GPIO14->GPIO15 loopback")
        print("Please connect GPIO14 directly to GPIO15")
        time.sleep(2)
        
        test_byte = b'U'  # 0x55 - alternating 1/0
        print(f"\nSending single byte: 0x{test_byte[0]:02X}")
        
        ser.write(test_byte)
        time.sleep(0.1)
        
        response = ser.read(1)
        if response:
            print(f"Received: 0x{response[0]:02X}")
            if response == test_byte:
                print("SUCCESS: Direct loopback working!")
            else:
                print("FAIL: Received different data")
        else:
            print("FAIL: No data received")
            
    finally:
        ser.close()
        print("\nTest completed")

if __name__ == "__main__":
    test_direct_loopback() 