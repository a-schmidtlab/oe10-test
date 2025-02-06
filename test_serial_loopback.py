from max3232 import MAX3232
import time

def test_serial_communication():
    device = MAX3232()
    
    commands = [
        ("Movement command 1 (Pan 0x08, Tilt 0x1E)", 
         "3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E"),
        
        ("Stop command 1", 
         "3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E"),
        
        ("Movement command 2 (Pan 0x04, Tilt 0x28)", 
         "3C 03 3A 01 3A 07 3A 50 43 3A 04 00 28 00 3A 3A 3A 47 3E"),
        
        ("Stop command 2", 
         "3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E")
    ]
    
    try:
        print("\nStarting serial communication test...")
        print("Please watch for received data on the other computer...")
        
        while True:
            for description, cmd in commands:
                print(f"\n\nSending: {description}")
                print(f"Hex: {cmd}")
                device.send_hex(cmd)
                
                # Wait longer to see response
                print("Waiting for response...")
                time.sleep(3)
                
                # Clear line
                print("-" * 50)
                time.sleep(2)
            
            # Ask if we should continue
            response = input("\nPress Enter to send commands again, or 'q' to quit: ")
            if response.lower() == 'q':
                break
                
    finally:
        # Send stop command before closing
        print("\nSending final stop command...")
        stop_cmd = "3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E"
        device.send_hex(stop_cmd)
        time.sleep(1)
        device.close()

if __name__ == "__main__":
    print("Testing serial communication between computers...")
    test_serial_communication()
    print("\nTest completed") 