import serial
import time

def test_serial():
    try:
        # Open serial port
        ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        
        print("Serial port opened successfully")
        print("Please watch the TX/RX LEDs on the MAX3232...")
        
        while True:
            # Send a simple test string
            test_data = "TEST\r\n"
            print(f"\nSending: {test_data!r}")
            ser.write(test_data.encode())
            ser.flush()
            
            # Wait and read response
            time.sleep(0.5)
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print(f"Received: {response!r}")
            else:
                print("No response")
            
            # Wait before next test
            time.sleep(2)
            
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    finally:
        if 'ser' in locals():
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    print("Simple serial test - Press Ctrl+C to stop")
    test_serial() 