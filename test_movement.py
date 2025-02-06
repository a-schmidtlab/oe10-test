from max3232 import MAX3232
import time

def test_movement():
    device = MAX3232()
    
    # The working proportional control command you provided
    # 3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E
    # This appears to be a proportional control command with:
    # - Pan speed: 0x00 (stopped)
    # - Tilt speed: 0x1E (30 in decimal, about 47% speed)
    
    try:
        # First, let's check status
        print("\n1. Checking status...")
        status_cmd = "3C FF 3A 01 3A 03 3A 53 54 3A 3A 7E 3A 47 3E"
        device.send_hex(status_cmd)
        time.sleep(1)
        
        # Now send the working movement command
        print("\n2. Sending movement command...")
        move_cmd = "3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E"
        device.send_hex(move_cmd)
        time.sleep(2)
        
        # Check status again
        print("\n3. Checking status after movement...")
        device.send_hex(status_cmd)
        time.sleep(1)
        
        # Stop movement
        print("\n4. Sending stop command...")
        stop_cmd = "3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 00 3A 47 3E"
        device.send_hex(stop_cmd)
        time.sleep(1)
        
    finally:
        device.close()

if __name__ == "__main__":
    print("Testing OE10 movement with hex commands...")
    test_movement()
    print("\nTest completed") 