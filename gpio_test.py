from gpiozero import LED
import time

# GPIO14 is TX, we'll toggle it to see if it's working
tx = LED(14)

print("Testing TX pin (GPIO14)...")
print("Please connect oscilloscope/multimeter to GPIO14")
print("You should see the voltage changing")

try:
    while True:
        tx.on()
        time.sleep(1)
        tx.off()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nTest stopped") 