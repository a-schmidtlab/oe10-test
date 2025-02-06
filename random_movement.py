from max3232 import MAX3232
import time
import random

def test_random_movements():
    device = MAX3232()
    
    # List of movement commands
    commands = [
        "3C 03 3A 01 3A 07 3A 50 43 3A 08 00 1E 00 3A 00 3A 47 3E",  # Movement 1
        "3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E",  # Stop
        "3C 03 3A 01 3A 07 3A 50 43 3A 04 00 28 00 3A 3A 3A 47 3E",  # Movement 2
        "3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E"   # Stop
    ]
    
    try:
        print("\nStarting random movement test...")
        
        # Send each command 3 times in random order
        for i in range(12):
            # Select random command
            cmd = random.choice(commands)
            
            print(f"\nMovement {i+1}:")
            device.send_hex(cmd)
            
            # Random delay between 1-3 seconds
            delay = random.uniform(1, 3)
            print(f"Waiting {delay:.1f} seconds...")
            time.sleep(delay)
            
    finally:
        # Always send stop command before closing
        stop_cmd = "3C 03 3A 01 3A 07 3A 50 43 3A 00 00 00 00 3A 16 3A 47 3E"
        print("\nSending final stop command...")
        device.send_hex(stop_cmd)
        time.sleep(1)
        device.close()

if __name__ == "__main__":
    print("Testing OE10 with random movement commands...")
    test_random_movements()
    print("\nTest completed") 