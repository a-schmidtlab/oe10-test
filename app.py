from flask import Flask, render_template, request, jsonify
from oe10_protocol import OE10Protocol
import logging
import sys

# Configure logging to show on console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global controller variable
controller = None

def init_controller():
    """Initialize the OE10 controller with error handling"""
    global controller
    try:
        if controller is None:
            logger.info("Initializing OE10 controller...")
            controller = OE10Protocol(port='/dev/ttyAMA0')  # Explicitly specify port
            logger.info("OE10 controller initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize OE10 controller: {str(e)}")
        return False

@app.route('/')
def index():
    """Render the main control interface"""
    if not init_controller():
        return render_template('index.html', 
                             error="Failed to initialize device connection. Check serial port and device.")
    
    try:
        status = controller.get_status()
        protocol_version = controller.get_protocol_version()
        software_version = controller.get_software_version()
        
        return render_template('index.html', 
                             status=status,
                             protocol_version=protocol_version,
                             software_version=software_version)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return render_template('index.html', error=str(e))

@app.route('/api/status')
def get_status():
    """Get current device status"""
    if not init_controller():
        return jsonify({"success": False, "error": "Device not initialized"})
    
    try:
        status = controller.get_status()
        if status is None:
            logger.warning("Failed to get status from device")
            return jsonify({"success": False, "error": "No status available"})
        return jsonify({"success": True, "status": status})
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/move', methods=['POST'])
def move():
    """Handle absolute position movement"""
    if not init_controller():
        return jsonify({"success": False, "error": "Device not initialized"})
    
    try:
        data = request.get_json()
        pan = float(data.get('pan')) if data.get('pan') is not None else None
        tilt = float(data.get('tilt')) if data.get('tilt') is not None else None
        
        success = True
        if pan is not None:
            success &= controller.move_pan_to(pan)
        if tilt is not None:
            success &= controller.move_tilt_to(tilt)
            
        return jsonify({"success": success})
    except Exception as e:
        logger.error(f"Error in move: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/proportional', methods=['POST'])
def proportional_control():
    """Handle proportional control movement"""
    if not init_controller():
        return jsonify({"success": False, "error": "Device not initialized"})
    
    try:
        data = request.get_json()
        success = controller.proportional_control(
            pan_direction=int(data.get('pan_direction', 0)),
            tilt_direction=int(data.get('tilt_direction', 0)),
            pan_speed=int(data.get('pan_speed', 50)),
            tilt_speed=int(data.get('tilt_speed', 50))
        )
        return jsonify({"success": success})
    except Exception as e:
        logger.error(f"Error in proportional control: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/stop', methods=['POST'])
def stop():
    """Stop all movement"""
    if not init_controller():
        return jsonify({"success": False, "error": "Device not initialized"})
    
    try:
        pan_stop = controller.pan_stop()
        tilt_stop = controller.tilt_stop()
        return jsonify({"success": pan_stop and tilt_stop})
    except Exception as e:
        logger.error(f"Error stopping movement: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/versions')
def get_versions():
    """Get protocol and software versions"""
    if not init_controller():
        return jsonify({"success": False, "error": "Device not initialized"})
    
    try:
        return jsonify({
            "success": True,
            "protocol_version": controller.get_protocol_version(),
            "software_version": controller.get_software_version()
        })
    except Exception as e:
        logger.error(f"Error getting versions: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the application and cleanup resources"""
    global controller
    try:
        if controller:
            controller.close()
            controller = None
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return jsonify({"success": True, "message": "Server shutting down..."})
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.teardown_appcontext
def cleanup(error):
    """Ensure proper cleanup on shutdown"""
    global controller
    if controller:
        controller.close()
        controller = None

@app.route('/api/debug_command', methods=['POST'])
def debug_command():
    """Send a raw command for debugging"""
    if not init_controller():
        return jsonify({"success": False, "error": "Device not initialized"})
    
    try:
        data = request.get_json()
        command = data.get('command')
        params = data.get('params', '')
        
        response = controller._send_command(command, params)
        return jsonify({
            "success": True,
            "sent_command": command,
            "sent_params": params,
            "response": response
        })
    except Exception as e:
        logger.error(f"Error in debug command: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/test_capture', methods=['POST'])
def test_capture():
    """Test exact captured commands"""
    if not init_controller():
        return jsonify({"success": False, "error": "Device not initialized"})
    
    try:
        data = request.get_json()
        direction = data.get('direction', 'stop')
        
        # Use exact captured commands
        if direction == 'up':
            cmd_data = "08001E00"
        elif direction == 'down':
            cmd_data = "0400280"
        elif direction == 'left':
            cmd_data = "023200000"
        elif direction == 'right':
            cmd_data = "013200000"
        else:  # stop
            cmd_data = "00000000"
            
        response = controller._send_command("PC", cmd_data)
        return jsonify({
            "success": True,
            "direction": direction,
            "data_sent": cmd_data,
            "response": response
        })
    except Exception as e:
        logger.error(f"Error in test capture: {e}")
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    logger.info("Starting Flask application...")
    try:
        # Try to initialize controller before starting server
        init_success = init_controller()
        if not init_success:
            logger.warning("Controller initialization failed, but continuing with web server startup")
        
        logger.info("Starting web server on port 5000...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        if controller:
            controller.close()
        sys.exit(1) 