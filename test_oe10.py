import serial
import time
import binascii
from struct import unpack

# Constants from Packet.hpp
ACK = 0x06
NAK = 0x15
CONTROLLER_ID = 0x01
PERIPHERAL_ID = 0x03

def compute_checksum(data):
    """Compute XOR checksum of data"""
    result = 0
    for b in data:
        result ^= b
    return result

def marshal_checksum(checksum):
    """Handle special checksum encoding"""
    if checksum == 0x3A or checksum == 0x3E:  # ':' or '>'
        return bytes([0x30, 0x30, checksum])  # '00' + checksum
    else:
        return bytes([checksum, 0x30, 0x30])  # checksum + '00'

def build_packet(to_addr, from_addr, command, data=b''):
    """Build a packet following the exact protocol"""
    packet = bytearray([0x3C])  # '<'
    packet.extend([to_addr, 0x3A, from_addr, 0x3A])
    packet.append(len(command) + len(data) + 1)
    packet.append(0x3A)
    packet.extend(command)
    packet.append(0x3A)
    if data:
        packet.extend(data)
        packet.append(0x3A)
    checksum = compute_checksum(packet[1:])
    packet.extend(marshal_checksum(checksum))
    packet.append(0x3E)
    return packet

def read_response(ser, timeout=1.0):
    """Read and parse a complete response packet"""
    start_time = time.time()
    buffer = bytearray()
    
    while (time.time() - start_time) < timeout:
        if ser.in_waiting:
            byte = ser.read()
            buffer.extend(byte)
            
            # Check if we have a complete packet
            if byte[0] == 0x3E and len(buffer) > 10:  # '>' and minimum packet size
                print(f"Raw response: {buffer.hex(' ')}")
                
                # Parse response
                if len(buffer) > 7 and buffer[7] == ACK:
                    print("Received ACK")
                    # Extract any data after ACK
                    if len(buffer) > 9:
                        data = buffer[9:-5]  # Skip header and checksum
                        print(f"Response data: {data.hex(' ')}")
                        return True, data
                    return True, None
                    
                elif len(buffer) > 7 and buffer[7] == NAK:
                    print("Received NAK")
                    if len(buffer) > 9:
                        error = buffer[9]
                        print(f"Error code: {error:02x}")
                    return False, None
                    
                return True, buffer
        time.sleep(0.01)
    
    print("No response received")
    return False, None

def decode_status(data):
    """Decode status response based on Status.hpp"""
    if not data or len(data) < 9:
        return None
        
    # First byte contains camera and PTU flags
    b0 = data[0]
    b1 = data[1]
    b2 = data[2]
    
    status = {
        'camera': {
            'enabled': bool(b0 & 0x01),
            'focus': bool(b0 & 0x02),
            'zoom': bool(b0 & 0x04),
            'auto_focus': bool(b0 & 0x20),
            'manual_exposure': bool(b0 & 0x40),
            'stills': bool(b0 & 0x80)
        },
        'ptu': {
            'pan': bool(b0 & 0x08),
            'tilt': bool(b0 & 0x10)
        },
        'temperature': ((b2 & 0x0F) * 5) - 5,
        'humidity': ((b2 >> 4) * 100) // 16
    }
    
    # Parse pan/tilt positions
    if len(data) >= 9:
        # Convert 3-byte position values to angles
        pan_bytes = data[3:6]
        tilt_bytes = data[6:9]
        try:
            pan_str = ''.join(chr(b) for b in pan_bytes if 0x30 <= b <= 0x39)
            tilt_str = ''.join(chr(b) for b in tilt_bytes if 0x30 <= b <= 0x39)
            status['pan'] = float(pan_str) if pan_str != '999' else 0
            status['tilt'] = float(tilt_str) if tilt_str != '999' else 0
        except ValueError:
            print(f"Error parsing positions: pan={pan_bytes.hex()} tilt={tilt_bytes.hex()}")
    
    return status

def test_movement():
    ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=2
    )

    try:
        print("\nQuerying device status...")
        
        # Send status request
        status_cmd = build_packet(PERIPHERAL_ID, CONTROLLER_ID, b'ST')
        print(f"Sending ST: {status_cmd.hex(' ')}")
        ser.write(status_cmd)
        success, data = read_response(ser)
        
        if success and data:
            status = decode_status(data)
            if status:
                print("\nDevice Status:")
                print(f"PTU: Pan={status['ptu']['pan']}, Tilt={status['ptu']['tilt']}")
                print(f"Temperature: {status['temperature']}°C")
                print(f"Humidity: {status['humidity']}%")
                print(f"Current position: Pan={status.get('pan', '?')}°, Tilt={status.get('tilt', '?')}°")
        
        print("\nTesting UP movement...")
        up_data = bytes([0x08, 0x00, 0x1E, 0x00])
        up_cmd = build_packet(PERIPHERAL_ID, CONTROLLER_ID, b'PC', up_data)
        print(f"Sending PC: {up_cmd.hex(' ')}")
        ser.write(up_cmd)
        success, _ = read_response(ser)
        
        if success:
            time.sleep(2)
            
            print("\nStopping movement...")
            stop_data = bytes([0x00, 0x00, 0x00, 0x00])
            stop_cmd = build_packet(PERIPHERAL_ID, CONTROLLER_ID, b'PC', stop_data)
            print(f"Sending PC: {stop_cmd.hex(' ')}")
            ser.write(stop_cmd)
            read_response(ser)

    finally:
        ser.close()
        print("\nPort closed")

if __name__ == "__main__":
    test_movement() 