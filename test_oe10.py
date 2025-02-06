from oe10_protocol import OE10Controller
import time

def test_oe10_detailed():
    print("Testing OE10 Controller with detailed output...")
    controller = OE10Controller()
    
    def send_raw_command(cmd, description=""):
        print(f"\nSending command: {description}")
        print(f"Raw command: {cmd!r}")
        controller.device.send(cmd)
        time.sleep(0.1)
        response = controller.device.read()
        print(f"Response: {response!r}")
        return response

    # Test basic communication
    print("\nTesting basic communication...")
    
    # First, check status
    send_raw_command("<FF:01:03:ST::7E:G>", "Check Status")
    time.sleep(1)
    
    # Move pan to 0 degrees
    send_raw_command("<FF:01:06:PP:000:04:G>", "Pan to 0°")
    time.sleep(2)
    
    # Move pan to +20 degrees
    send_raw_command("<FF:01:06:PP:020:05:G>", "Pan to +20°")
    time.sleep(2)
    
    # Move pan back to 0 degrees
    send_raw_command("<FF:01:06:PP:000:04:G>", "Pan back to 0°")
    time.sleep(2)
    
    # Move pan to -20 degrees
    send_raw_command("<FF:01:06:PP:340:03:G>", "Pan to -20° (340°)")
    time.sleep(2)
    
    # Finally move back to center
    send_raw_command("<FF:01:06:PP:000:04:G>", "Pan to center")
    time.sleep(2)
    
    controller.close_connection()
    print("\nTest completed")

if __name__ == "__main__":
    test_oe10_detailed() 