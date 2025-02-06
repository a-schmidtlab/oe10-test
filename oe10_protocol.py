from max3232 import MAX3232

class OE10Controller:
    def __init__(self, port='/dev/ttyUSB0'):
        self.device = MAX3232(port=port)
        self.current_pan = 0
        self.current_tilt = 0

    def move(self, pan=None, tilt=None):
        """
        Send a command to move the pan/tilt unit.
        """
        command = []
        if pan is not None:
            command.append(f"PAN:{pan}")
            self.current_pan = pan
        if tilt is not None:
            command.append(f"TILT:{tilt}")
            self.current_tilt = tilt

        if command:
            command_str = ",".join(command) + "\n"
            self.device.send(command_str)
            return self.device.read()
        return "No movement parameters provided"

    def get_status(self):
        """Get the current status from the OE10 device."""
        self.device.send("STATUS?\n")
        status = self.device.read()
        if not status:
            status = f"Current Position - Pan: {self.current_pan}°, Tilt: {self.current_tilt}°"
        return status

    def debug_info(self):
        """Return any debug information from the device."""
        self.device.send("DEBUG?\n")
        debug = self.device.read()
        if not debug:
            debug = "No debug information available"
        return debug

    def close_connection(self):
        self.device.close()

if __name__ == "__main__":
    controller = OE10Controller()
    print("Moving device...")
    print("Response:", controller.move(pan=45, tilt=30))
    print("Status:", controller.get_status())
    controller.close_connection() 