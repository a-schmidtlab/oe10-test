from oe10_protocol import OE10Controller
import time

def test_oe10_detailed():
    print("Testing OE10 Controller with detailed output...")
    controller = OE10Controller()
    
    def send_raw_command(cmd, description=""):
        print(f"\nSending command: {description}")
        print(f"Raw command: {cmd!r}")
        controller.device.send(cmd)
        time.sleep(0.1)  # Small delay for device processing
        response = controller.device.read()
        print(f"Response: {response!r}")
        return response

    # Test basic communication
    print("\n1. Testing basic communication...")
    
    # First, check protocol version
    print("\nChecking protocol version...")
    send_raw_command("<FF:01:03:PV::7D:G>", "Protocol Version Request")
    time.sleep(1)
    
    # Check status
    print("\nChecking device status...")
    send_raw_command("<FF:01:03:ST::7E:G>", "Status Request")
    time.sleep(1)
    
    # Get error diagnosis
    print("\nChecking for any errors...")
    send_raw_command("<FF:01:03:ED::6C:G>", "Error Diagnosis Request")
    time.sleep(1)
    
    print("\n2. Testing pan movement...")
    
    # Enable end stops first
    print("\nEnabling end stops...")
    send_raw_command("<FF:01:04:ES:1:72:G>", "Enable End Stops")
    time.sleep(1)
    
    # Move pan to 0 degrees
    print("\nMoving pan to 0°...")
    send_raw_command("<FF:01:06:PP:000:04:G>", "Pan to 0°")
    time.sleep(3)  # Give more time for movement
    
    # Check position after movement
    send_raw_command("<FF:01:03:ST::7E:G>", "Status Check after Pan 0°")
    time.sleep(1)
    
    # Move pan to +20 degrees
    print("\nMoving pan to +20°...")
    send_raw_command("<FF:01:06:PP:020:05:G>", "Pan to +20°")
    time.sleep(3)
    
    # Check position after movement
    send_raw_command("<FF:01:03:ST::7E:G>", "Status Check after Pan +20°")
    time.sleep(1)
    
    print("\n3. Testing tilt movement...")
    
    # Move tilt to 0 degrees
    print("\nMoving tilt to 0°...")
    send_raw_command("<FF:01:06:TP:000:05:G>", "Tilt to 0°")
    time.sleep(3)
    
    # Check position after movement
    send_raw_command("<FF:01:03:ST::7E:G>", "Status Check after Tilt 0°")
    time.sleep(1)
    
    # Move tilt to +30 degrees
    print("\nMoving tilt to +30°...")
    send_raw_command("<FF:01:06:TP:030:07:G>", "Tilt to +30°")
    time.sleep(3)
    
    # Check position after movement
    send_raw_command("<FF:01:03:ST::7E:G>", "Status Check after Tilt +30°")
    time.sleep(1)
    
    # Final status check
    print("\n4. Final status check...")
    send_raw_command("<FF:01:03:ST::7E:G>", "Final Status Check")
    
    controller.close_connection()
    print("\nTest completed")

if __name__ == "__main__":
    test_oe10_detailed() 