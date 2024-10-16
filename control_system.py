from datetime import datetime
import pickle
class EEGControlSystem:
    """Initializes the EEG Control System with empty lists of amplifiers and sensors."""
    def __init__(self):
        self.amplifiers = []
        self.sensors = []
    
    """ Save the current state of amplifiers and sensors to a file """
    def save_state(self, filename="amplifier_repository.pkl"):
        with open(filename, 'wb') as f:
            pickle.dump({
                "amplifiers": self.amplifiers,
                "sensors": self.sensors
            }, f)
        print(f"State saved to {filename}")

    """ Load the state of amplifiers and sensors from a file """
    def load_state(self, filename="amplifier_repository.pkl"):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.amplifiers = data.get("amplifiers", [])
                self.sensors = data.get("sensors", [])
            print(f"State loaded from {filename}")
        except FileNotFoundError:
            print(f"No saved state found. Starting fresh.")
    
    def find_amplifier(self, serial_number):
        """Finds and returns an amplifier by its serial number."""
        for amp in self.amplifiers:
            if amp.serial_number == serial_number:
                return amp
        return None

    def find_sensor(self, serial_number):
        """Finds and returns a sensor by its serial number."""
        for sensor in self.sensors:
            if sensor.serial_number == serial_number:
                return sensor
        return None

    def add_amplifier(self, amplifier):
        """Adds a new amplifier to the system."""
        self.amplifiers.append(amplifier)
        print(f"Amplifier with serial number {amplifier.serial_number} added.")

    def remove_amplifier(self, serial_number):
        """Removes an amplifier from the system by its serial number."""
        amplifier_to_remove = None
        for amplifier in self.amplifiers:
            if amplifier.serial_number == serial_number:
                amplifier_to_remove = amplifier
                break
        
        if amplifier_to_remove:
            self.amplifiers.remove(amplifier_to_remove)
            print(f"Amplifier with serial number {serial_number} removed.")
        else:
            print(f"Amplifier with serial number {serial_number} not found.")

    def list_amplifiers(self):
        """Returns a list of all amplifiers in the system."""
        return self.amplifiers

    def search_amplifiers(self, query, search_by="serial_number"):
        """Searches amplifiers based on serial number, model, or manufacturer and returns the founding amplifiers."""
        results = []
        if search_by == "serial_number":
            results = [amp for amp in self.amplifiers if amp.serial_number == query]
        elif search_by == "model_string":
            results = [amp for amp in self.amplifiers if query.lower() in amp.model_string.lower()]
        elif search_by == "manufacturer":
            results = [amp for amp in self.amplifiers if query.lower() in amp.manufacturer.lower()]
        
        return results
    
    def add_sensor(self, sensor):
        """Adds a new sensor to the system."""
        self.sensors.append(sensor)
        print(f"Amplifier with serial number {sensor.serial_number} added.")

    def add_sensor_to_amplifier(self, amplifier_serial, sensor_serial):
        """Adds an existing sensor to an amplifier. If there is not such sensor, raises error."""
        amplifier = self.find_amplifier(amplifier_serial)
        if amplifier:
            sensor = self.find_sensor(sensor_serial)
            if sensor:
                amplifier.add_sensor(sensor)
                print(f"Sensor {sensor_serial} added to Amplifier {amplifier_serial}")
            else:
                print(f"Sensor {sensor_serial} not found in the system. Please add it first.")
        else:
            print(f"Amplifier {amplifier_serial} not found.")

    def remove_sensor_from_amplifier(self, amplifier_serial, sensor_serial):
        """Removes a sensor from an amplifier."""
        amplifier = self.find_amplifier(amplifier_serial)
        if amplifier:
            sensor_to_remove = None
            for sensor in amplifier.sensors:
                if sensor.serial_number == sensor_serial:
                    sensor_to_remove = sensor
                    break
            
            if sensor_to_remove:
                amplifier.remove_sensor(sensor_to_remove)
                print(f"Sensor {sensor_serial} removed from Amplifier {amplifier_serial}")
            else:
                print(f"Sensor {sensor_serial} not found in this amplifier.")
        else:
            print(f"Amplifier {amplifier_serial} not found.")
    
    def update_maintenance_date(self, device, new_date):
        """Updates the next maintenance date for a given device."""
        try:
            # Parse the new date and check if it's in the future
            parsed_date = datetime.strptime(new_date, "%d-%m-%Y")
            if parsed_date > datetime.now():
                device.next_maintenance = new_date
                print(f"Maintenance date updated to {new_date}.")
            else:
                print("Error: Maintenance date must be in the future.")
        except ValueError:
            print("Error: Invalid date format. Use DD-MM-YYYY.")

