import serial
import time

def test_with_debug():
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=2  # Increased timeout
    )
    
    try:
        print("Starting debug test...")
        print(f"Port: {ser.name}")
        print(f"Settings: {ser.get_settings()}")
        
        # Clear any existing data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Test 1: Status command with detailed debugging
        command = b"<FF:01:03:ST::7E:G>"
        print(f"\nSending command (hex): {command.hex()}")
        print(f"Command length: {len(command)} bytes")
        
        # Send byte by byte with delay
        for byte in command:
            ser.write(bytes([byte]))
            print(f"Sent byte: 0x{byte:02X}")
            time.sleep(0.01)  # 10ms delay between bytes
        
        print("\nWaiting for response...")
        # Check for response multiple times
        for i in range(5):
            time.sleep(0.5)  # 500ms between checks
            if ser.in_waiting:
                response = ser.read(ser.in_waiting)
                print(f"Response received after {(i+1)*0.5}s:")
                print(f"  Hex: {response.hex()}")
                print(f"  ASCII: {response}")
                print(f"  Bytes: {[hex(b) for b in response]}")
            else:
                print(f"No data after {(i+1)*0.5}s")
        
        # Check serial port status
        print("\nPort Status:")
        print(f"CTS: {ser.cts}")
        print(f"DSR: {ser.dsr}")
        print(f"CD: {ser.cd}")
        print(f"RI: {ser.ri}")
        print(f"In waiting: {ser.in_waiting}")
        print(f"Out waiting: {ser.out_waiting}")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        
    finally:
        ser.close()
        print("\nPort closed")

if __name__ == "__main__":
    test_with_debug() 