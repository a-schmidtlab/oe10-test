import serial
import time
import binascii

def test_serial():
    # Open port
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    
    try:
        print("Opening port and waiting 2 seconds...")
        time.sleep(2)  # Give device time to initialize
        
        # Clear any pending data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Test 1: Simple ASCII
        print("\nTest 1: Sending simple ASCII...")
        ser.write(b'TEST\r\n')
        time.sleep(0.5)
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print(f"Response: {response}")
        
        # Test 2: Status command from hexdump (single byte at a time)
        print("\nTest 2: Sending status command byte by byte...")
        status_bytes = bytes.fromhex('3c 03 3a 01 3a 03 3a 53 54 3a 3a 06 3a 47 3e'.replace(' ', ''))
        for b in status_bytes:
            ser.write(bytes([b]))
            time.sleep(0.01)  # Small delay between bytes
            print(f"Sent byte: {hex(b)}")
            if ser.in_waiting:
                resp = ser.read(ser.in_waiting)
                print(f"Got response: {resp.hex()}")
        
        # Wait for final response
        time.sleep(0.5)
        while ser.in_waiting:
            resp = ser.read(ser.in_waiting)
            print(f"Final response: {resp.hex()}")
        
        # Test 3: Monitor incoming data
        print("\nTest 3: Monitoring incoming data for 5 seconds...")
        start_time = time.time()
        while (time.time() - start_time) < 5:
            if ser.in_waiting:
                data = ser.read(ser.in_waiting)
                print(f"Received: {data.hex()}")
            time.sleep(0.1)
            
    finally:
        ser.close()
        print("\nPort closed")

if __name__ == "__main__":
    test_serial() 