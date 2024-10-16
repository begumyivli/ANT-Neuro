# Begum Yivli ANT-Neuro Task
## 1. Running the Program via main.py
Prerequisites: Python 3.11 installed.
   
How to Run:
    1. Clone or download this repository.
    2. Open a terminal in the project directory.
    3. Run the main program:
    
    python main.py

## 2. Running the Program via control_system_api.py (RESTful API)
Prerequisites:
Python 3.11 installed.
Flask installed. You can install it using:
    
    pip install flask
    
How to Run the API:
    Clone or download this repository.
    Open a terminal in the project directory.
    Run the API server:
    
    python control_system_api.py
The server will start at http://127.0.0.1:5000.

### API Endpoints:
**Add Amplifier (POST):**
curl -X POST http://127.0.0.1:5000/api/amplifiers -H "Content-Type: application/json" -d '{
  "serial_number": "A001",
  "model_string": "ModelX",
  "manufacturer": "AMD",
  "next_maintenance": "01-12-2024",
  "sampling_rate": 512,
  "gain": 5
}'

**Get All Amplifiers (GET):**
curl -X GET http://127.0.0.1:5000/api/amplifiers

**Remove Amplifier (DELETE):**
curl -X DELETE http://127.0.0.1:5000/api/amplifiers/A001

**Set Gain (PUT):**
curl -X PUT http://127.0.0.1:5000/api/amplifiers/A001/gain -H "Content-Type: application/json" -d '{
  "gain": 10
}'

**Set Sampling Rate (PUT):**
curl -X PUT http://127.0.0.1:5000/api/amplifiers/A001/sampling_rate -H "Content-Type: application/json" -d '{
  "sampling_rate": 1024
}'

**Toggle Power (POST):**
curl -X POST http://127.0.0.1:5000/api/amplifiers/A001/power

**Add Sensor (POST):**
curl -X POST http://127.0.0.1:5000/api/sensors -H "Content-Type: application/json" -d '{
  "serial_number": "S001",
  "model_string": "SensorX",
  "manufacturer": "AMD",
  "next_maintenance": "01-12-2024",
  "tag": "frontal"
}'

**Add Sensor to Amplifier (POST):**
curl -X POST http://127.0.0.1:5000/api/amplifiers/A001/sensors -H "Content-Type: application/json" -d '{
  "sensor_serial": "S001"
}'

**Remove Sensor from Amplifier (DELETE):**
curl -X DELETE http://127.0.0.1:5000/api/amplifiers/A001/sensors/S001

**Update Maintenance Date (PUT):**
curl -X PUT http://127.0.0.1:5000/api/device/amplifier/A001/maintenance -H "Content-Type: application/json" -d '{
  "new_date": "2025-01-01"
}'

