import serial
import time
import binascii

def test_uart():
    try:
        # Configure port
        ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        
        print("Port opened successfully")
        
        def send_and_receive(cmd, description):
            print(f"\nSending {description}")
            print(f"TX: {binascii.hexlify(cmd).decode()}")
            ser.reset_input_buffer()  # Clear any pending input
            ser.write(cmd)
            time.sleep(0.5)
            
            # Read with timeout
            response = b''
            start_time = time.time()
            while time.time() - start_time < 1.0:  # 1 second timeout
                if ser.in_waiting:
                    response += ser.read(ser.in_waiting)
                    time.sleep(0.1)
            
            if response:
                print(f"RX: {binascii.hexlify(response).decode()}")
            else:
                print("No response received")
            return response

        # Test 1: Status Request
        status_cmd = bytes.fromhex('3C FF 01 03 53 54 3A 3A 7E 47 3E')
        send_and_receive(status_cmd, "Status Request")
        
        # Test 2: Pan Stop (safe command)
        stop_cmd = bytes.fromhex('3C FF 01 03 50 53 3A 3A 7C 47 3E')
        send_and_receive(stop_cmd, "Pan Stop")
        
        # Test 3: Simple Pan Left command with slower speed
        # Set pan speed to 25% first
        speed_cmd = bytes.fromhex('3C FF 01 04 44 53 3A 19 3A 7B 47 3E')  # DS command with speed 25
        send_and_receive(speed_cmd, "Set Pan Speed 25%")
        
        # Then pan left
        left_cmd = bytes.fromhex('3C FF 01 03 50 4C 3A 3A 7D 47 3E')
        send_and_receive(left_cmd, "Pan Left")
        
        time.sleep(2)  # Let it move for 2 seconds
        
        # Stop
        send_and_receive(stop_cmd, "Pan Stop")
            
        # Test TX/RX lines
        print("\nTesting TX/RX lines:")
        print(f"CTS: {ser.cts}")
        print(f"DSR: {ser.dsr}")
        print(f"CD: {ser.cd}")
        print(f"RI: {ser.ri}")
        
        ser.close()
        print("\nPort closed")
        
    except serial.SerialException as e:
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check if UART is enabled in /boot/config.txt")
        print("2. Check if user is in dialout group")
        print("3. Check physical connections (TX->RX, RX->TX, GND->GND)")
        print("4. Verify voltage levels (MAX3232 converts RS-232 to TTL)")

if __name__ == "__main__":
    test_uart() 