class EEGControlSystem:
    def __init__(self):
        self.amplifiers = []
    
    def find_amplifier(self, serial_number):
        for amp in self.amplifiers:
            if amp.serial_number == serial_number:
                return amp
        return None

    def add_amplifier(self, amplifier):
        self.amplifiers.append(amplifier)
        print(f"Amplifier with serial number {amplifier.serial_number} added.")

    def remove_amplifier(self, serial_number):
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
        return self.amplifiers

    def search_amplifiers(self, query, search_by="serial_number"):
        results = []
        if search_by == "serial_number":
            results = [amp for amp in self.amplifiers if amp.serial_number == query]
        elif search_by == "model_string":
            results = [amp for amp in self.amplifiers if query.lower() in amp.model_string.lower()]
        elif search_by == "manufacturer":
            results = [amp for amp in self.amplifiers if query.lower() in amp.manufacturer.lower()]
        
        return results

    def add_sensor_to_amplifier(self, amplifier_serial, sensor):
        amplifier = self.find_amplifier(amplifier_serial)
        if amplifier:
            amplifier.add_sensor(sensor)
            print(f"Sensor {sensor.serial_number} added to Amplifier {amplifier_serial}")
        else:
            print("Amplifier not found")

    def remove_sensor_from_amplifier(self, amplifier_serial, sensor_serial):
        amplifier = self.find_amplifier(amplifier_serial)
        if amplifier:
            sensor = next((s for s in amplifier.sensors if s.serial_number == sensor_serial), None)
            if sensor:
                amplifier.remove_sensor(sensor)
                print(f"Sensor {sensor_serial} removed from Amplifier {amplifier_serial}")
            else:
                print("Sensor not found in this amplifier")
        else:
            print("Amplifier not found")
