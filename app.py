from flask import Flask, render_template, request, jsonify
from oe10_protocol import OE10Controller

app = Flask(__name__)
controller = OE10Controller()  # Adjust port if needed

@app.route('/')
def index():
    # Render the main page
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    try:
        # Read the pan and tilt values from POST data
        pan = float(request.form.get('pan')) if request.form.get('pan') else None
        tilt = float(request.form.get('tilt')) if request.form.get('tilt') else None
        
        # Issue move command and capture response
        result = controller.move(pan=pan, tilt=tilt)
        return jsonify({"success": True, "response": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/pan_left', methods=['POST'])
def pan_left():
    try:
        result = controller.pan_left()
        return jsonify({"success": True, "response": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/pan_right', methods=['POST'])
def pan_right():
    try:
        result = controller.pan_right()
        return jsonify({"success": True, "response": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/pan_stop', methods=['POST'])
def pan_stop():
    try:
        result = controller.pan_stop()
        return jsonify({"success": True, "response": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/tilt_up', methods=['POST'])
def tilt_up():
    try:
        result = controller.tilt_up()
        return jsonify({"success": True, "response": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/tilt_down', methods=['POST'])
def tilt_down():
    try:
        result = controller.tilt_down()
        return jsonify({"success": True, "response": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/tilt_stop', methods=['POST'])
def tilt_stop():
    try:
        result = controller.tilt_stop()
        return jsonify({"success": True, "response": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/status', methods=['GET'])
def status():
    try:
        # Return the current status and debug information
        status = controller.get_status()
        return jsonify({"success": True, "status": status})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/protocol_version')
def protocol_version():
    try:
        version = controller.get_protocol_version()
        return jsonify({"success": True, "version": version})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/software_version')
def software_version():
    try:
        version = controller.get_software_version()
        return jsonify({"success": True, "version": version})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/debug')
def debug():
    try:
        info = controller.debug_info()
        return jsonify({"success": True, "info": info})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        # Endpoint to safely shutdown the device connection if needed
        controller.close_connection()
        return jsonify({"success": True, "message": "Device connection closed."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 