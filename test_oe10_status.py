#!/usr/bin/env python3

import serial
import time

def send_command(ser, command_hex):
    """Send a hex command and read response"""
    try:
        # Convert space-separated hex string to bytes
        command_bytes = bytes.fromhex(command_hex.replace(" ", ""))
        
        # Clear any existing data
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        
        # Send each byte with a small delay
        print("Sending bytes:", end=' ')
        for byte in command_bytes:
            ser.write(bytes([byte]))
            print(f"{byte:02X}", end=' ', flush=True)
            time.sleep(0.001)  # 1ms delay between bytes
        print(f"\nSent {len(command_bytes)} bytes")
        
        # Ensure all data is written
        ser.flush()
        time.sleep(0.1)  # Wait for transmission to complete
        
        # Read response if available
        if ser.in_waiting:
            response = bytearray()
            while ser.in_waiting:
                byte = ser.read()
                response.extend(byte)
                print(f"Received byte: {byte[0]:02X}")
                if byte == b'>':  # End of message marker
                    break
                time.sleep(0.001)
            
            if response:
                print(f"Complete response: {' '.join(f'{b:02X}' for b in response)}")
                try:
                    print(f"Decoded response: {response.decode()}")
                except UnicodeDecodeError:
                    print("Could not decode response as ASCII")
            else:
                print("No response received")
        else:
            print("No response received")
            
    except Exception as e:
        print(f"Error sending command: {e}")

def main():
    # Configure serial port
    try:
        ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1,
            xonxoff=False,    # Disable software flow control
            rtscts=False,     # Disable hardware flow control
            dsrdtr=False      # Disable hardware flow control
        )
        
        # Set RTS and DTR
        ser.setRTS(True)
        ser.setDTR(True)
        
        print("Serial port opened successfully")
        print(f"Port settings: {ser.get_settings()}")
        
        # The specific command to test
        test_command = "3C 03 3A 01 3A 07 3A 50 43 3A 04 00 28 00 3A 3A 3A 47 3E"
        
        while True:
            try:
                print("\n--- Sending test command ---")
                send_command(ser, test_command)
                
                # Wait before sending again
                time.sleep(2)
                
            except KeyboardInterrupt:
                print("\nTest terminated by user")
                break
            except Exception as e:
                print(f"Error during communication: {e}")
                break
                
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")

if __name__ == "__main__":
    main() 