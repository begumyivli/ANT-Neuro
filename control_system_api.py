from flask import Flask, request, jsonify
from control_system import EEGControlSystem
from amplifier import Amplifier
from sensor import Sensor

app = Flask(__name__)
control_system = EEGControlSystem()

control_system.load_state()

# simple welcome message
@app.route('/')
def home():
    return """
    <h1>EEG Control System API</h1>
    <p>Welcome to the EEG Control System API by Begum Yivli. Use the following endpoints to interact with the system:</p>
    <ul>
        <li><strong>GET /api/amplifiers</strong> - List all amplifiers</li>
        <li><strong>POST /api/amplifiers</strong> - Add an amplifier</li>
        <li><strong>DELETE /api/amplifiers/&lt;serial_number&gt;</strong> - Remove an amplifier</li>
        <li><strong>PUT /api/amplifiers/&lt;serial_number&gt;/gain</strong> - Set amplifier gain</li>
        <li><strong>PUT /api/amplifiers/&lt;serial_number&gt;/sampling_rate</strong> - Set amplifier sampling rate</li>
        <li><strong>POST /api/amplifiers/&lt;serial_number&gt;/power</strong> - Toggle amplifier power</li>
        <li><strong>GET /api/amplifiers/search</strong> - Search for amplifiers by serial_number, model_string, or manufacturer</li>
        <li><strong>POST /api/sensors</strong> - Add a sensor</li>
        <li><strong>POST /api/amplifiers/&lt;amplifier_serial&gt;/sensors</strong> - Add a sensor to an amplifier</li>
        <li><strong>DELETE /api/amplifiers/&lt;amplifier_serial&gt;/sensors/&lt;sensor_serial&gt;</strong> - Remove a sensor from an amplifier</li>
        <li><strong>PUT /api/device/&lt;device_type&gt;/&lt;serial_number&gt;/maintenance</strong> - Update a device's maintenance date</li>
        <li><strong>POST /api/save</strong> - Save the current system state</li>
        <li><strong>POST /api/load</strong> - Load the saved system state</li>
    </ul>
    """

# API Endpoint to add an amplifier
@app.route('/api/amplifiers', methods=['POST'])
def add_amplifier():
    data = request.json
    try:
        amplifier = Amplifier(
            serial_number=data['serial_number'],
            model_string=data['model_string'],
            manufacturer=data['manufacturer'],
            next_maintenance=data['next_maintenance'],
            sampling_rate=data['sampling_rate'],
            gain=data['gain']
        )
        control_system.add_amplifier(amplifier)
        return jsonify({"message": f"Amplifier {amplifier.serial_number} added successfully."}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing parameter: {str(e)}"}), 400

# API Endpoint to get all amplifiers
@app.route('/api/amplifiers', methods=['GET'])
def get_amplifiers():
    amplifiers = control_system.list_amplifiers()
    return jsonify([{
        "serial_number": amp.serial_number,
        "model_string": amp.model_string,
        "manufacturer": amp.manufacturer,
        "next_maintenance": amp.next_maintenance,
        "sampling_rate": amp.sampling_rate,
        "gain": amp.gain,
        "status": "On" if amp.is_on else "Off",
        "sensors": [sensor.serial_number for sensor in amp.sensors]
    } for amp in amplifiers]), 200

# API Endpoint to remove an amplifier
@app.route('/api/amplifiers/<serial_number>', methods=['DELETE'])
def remove_amplifier(serial_number):
    control_system.remove_amplifier(serial_number)
    return jsonify({"message": f"Amplifier {serial_number} removed."}), 200

# API Endpoint to set amplifier gain
@app.route('/api/amplifiers/<serial_number>/gain', methods=['PUT'])
def set_amplifier_gain(serial_number):
    amplifier = control_system.find_amplifier(serial_number)
    if amplifier:
        new_gain = request.json['gain']
        try:
            amplifier.set_gain(new_gain)
            return jsonify({"message": f"Amplifier {serial_number} gain set to {new_gain}."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Amplifier not found."}), 404

# API Endpoint to set amplifier sampling rate
@app.route('/api/amplifiers/<serial_number>/sampling_rate', methods=['PUT'])
def set_amplifier_sampling_rate(serial_number):
    amplifier = control_system.find_amplifier(serial_number)
    if amplifier:
        new_sampling_rate = request.json['sampling_rate']
        try:
            amplifier.set_sampling_rate(new_sampling_rate)
            return jsonify({"message": f"Amplifier {serial_number} sampling rate set to {new_sampling_rate} Hz."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    return jsonify({"error": "Amplifier not found."}), 404

# API Endpoint to toggle amplifier power
@app.route('/api/amplifiers/<serial_number>/power', methods=['POST'])
def toggle_amplifier_power(serial_number):
    amplifier = control_system.find_amplifier(serial_number)
    if amplifier:
        if amplifier.is_on:
            amplifier.power_off()
            return jsonify({"message": f"Amplifier {serial_number} powered off."}), 200
        else:
            amplifier.power_on()
            return jsonify({"message": f"Amplifier {serial_number} powered on."}), 200
    return jsonify({"error": "Amplifier not found."}), 404

# API Endpoint to search for amplifiers based on query parameters
@app.route('/api/amplifiers/search', methods=['GET'])
def search_amplifiers():
    serial_number = request.args.get('serial_number')
    model_string = request.args.get('model_string')
    manufacturer = request.args.get('manufacturer')

    results = control_system.amplifiers

    if serial_number:
        results = [amp for amp in results if serial_number.lower() in amp.serial_number.lower()]
    if model_string:
        results = [amp for amp in results if model_string.lower() in amp.model_string.lower()]
    if manufacturer:
        results = [amp for amp in results if manufacturer.lower() in amp.manufacturer.lower()]

    if not results:
        return jsonify({"message": "No amplifiers found."}), 404

    return jsonify([{
        "serial_number": amp.serial_number,
        "model_string": amp.model_string,
        "manufacturer": amp.manufacturer,
        "next_maintenance": amp.next_maintenance,
        "sampling_rate": amp.sampling_rate,
        "gain": amp.gain,
        "status": "On" if amp.is_on else "Off",
        "sensors": [sensor.serial_number for sensor in amp.sensors]
    } for amp in results]), 200

# API Endpoint to add a sensor to an amplifier
@app.route('/api/amplifiers/<amplifier_serial>/sensors', methods=['POST'])
def add_sensor_to_amplifier(amplifier_serial):
    data = request.json
    sensor_serial = data['sensor_serial']
    
    control_system.add_sensor_to_amplifier(amplifier_serial, sensor_serial)
    return jsonify({"message": f"Sensor {sensor_serial} added to Amplifier {amplifier_serial}."}), 201

# API Endpoint to add a sensor
@app.route('/api/sensors', methods=['POST'])
def add_sensor():
    data = request.json
    sensor = Sensor(
        serial_number=data['serial_number'],
        model_string=data['model_string'],
        manufacturer=data['manufacturer'],
        next_maintenance=data['next_maintenance'],
        tag=data['tag']
    )
    control_system.add_sensor(sensor)
    return jsonify({"message": f"Sensor {sensor.serial_number} added successfully."}), 201

# API Endpoint to remove a sensor from an amplifier
@app.route('/api/amplifiers/<amplifier_serial>/sensors/<sensor_serial>', methods=['DELETE'])
def remove_sensor_from_amplifier(amplifier_serial, sensor_serial):
    control_system.remove_sensor_from_amplifier(amplifier_serial, sensor_serial)
    return jsonify({"message": f"Sensor {sensor_serial} removed from Amplifier {amplifier_serial}."}), 200

# API Endpoint to save the current state
@app.route('/api/save', methods=['POST'])
def save_state():
    control_system.save_state()
    return jsonify({"message": "System state saved successfully."}), 200

# API Endpoint to load the saved state
@app.route('/api/load', methods=['POST'])
def load_state():
    control_system.load_state()
    return jsonify({"message": "System state loaded successfully."}), 200

# API Endpoint to update maintenance date for a device
@app.route('/api/device/<device_type>/<serial_number>/maintenance', methods=['PUT'])
def update_maintenance(device_type, serial_number):
    new_date = request.json['new_date']
    if device_type == "amplifier":
        amplifier = control_system.find_amplifier(serial_number)
        if amplifier:
            control_system.update_maintenance_date(amplifier, new_date)
            return jsonify({"message": f"Maintenance date updated for Amplifier {serial_number}."}), 200
        return jsonify({"error": "Amplifier not found."}), 404
    elif device_type == "sensor":
        sensor = control_system.find_sensor(serial_number)
        if sensor:
            control_system.update_maintenance_date(sensor, new_date)
            return jsonify({"message": f"Maintenance date updated for Sensor {serial_number}."}), 200
        return jsonify({"error": "Sensor not found."}), 404
    else:
        return jsonify({"error": "Invalid device type."}), 400

if __name__ == '__main__':
    app.run(debug=True)
