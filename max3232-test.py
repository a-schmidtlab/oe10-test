#!/usr/bin/env python3

import serial
import time

def main():
    # Configure the serial port
    # Usually /dev/ttyAMA0 for RPi5's UART pins
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )

    try:
        while True:
            # Send "Hello Reuters" message
            message = "Hello Reuters\r\n"
            ser.write(message.encode())
            print(f"Sent: {message.strip()}")
            
            # Wait for 1 second before sending again
            time.sleep(1)
            
            # Try to read any response (if connected to a loopback)
            if ser.in_waiting:
                received = ser.readline().decode().strip()
                print(f"Received: {received}")

    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    finally:
        ser.close()
        print("Serial port closed")

if __name__ == "__main__":
    main()
