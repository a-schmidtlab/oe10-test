import serial
import time
import sys
import os

def check_port_available(port):
    """Check if the port is available"""
    try:
        # Try to open the port
        ser = serial.Serial(port)
        ser.close()
        return True
    except serial.SerialException as e:
        print(f"Port {port} is not available: {str(e)}")
        return False

def test_serial_connection():
    PORT = '/dev/ttyAMA0'
    
    # Check if port exists
    if not os.path.exists(PORT):
        print(f"Error: {PORT} does not exist!")
        return
    
    # Check if port is available
    if not check_port_available(PORT):
        print("Please ensure no other program is using the port")
        print("Try running: sudo pkill picocom")
        return
    
    try:
        # Open port with explicit settings
        ser = serial.Serial(
            port=PORT,
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=2,
            exclusive=True  # Request exclusive access
        )
        
        print(f"Successfully opened {PORT}")
        print("Port settings:", ser.get_settings())
        
        # Clear buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Test sequence
        test_sequences = [
            (b"<FF:01:03:ST::7E:G>", "Status Request"),
            (b"<FF:01:06:PP:000:04:G>", "Pan to 0 degrees"),
        ]
        
        for command, description in test_sequences:
            print(f"\nSending {description}")
            print(f"Command (hex): {command.hex()}")
            
            # Send command
            ser.write(command)
            ser.flush()  # Ensure all data is written
            
            # Wait and check for response
            print("Waiting for response...")
            time.sleep(1)
            
            # Try to read response
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print("Response received:")
                print(f"  Hex: {response.hex()}")
                print(f"  ASCII: {response}")
                print(f"  Bytes: {[hex(b) for b in response]}")
            else:
                print("No response received")
            
            # Short pause between commands
            time.sleep(0.5)
        
    except serial.SerialException as e:
        print(f"Serial error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("\nPort closed")

if __name__ == "__main__":
    test_serial_connection() 