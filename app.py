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
        response = controller.move(pan=pan, tilt=tilt)
        return jsonify({"success": True, "response": response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/status', methods=['GET'])
def status():
    try:
        # Return the current status and debug information
        status = controller.get_status()
        debug = controller.debug_info()
        return jsonify({
            "success": True,
            "status": status,
            "debug": debug
        })
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