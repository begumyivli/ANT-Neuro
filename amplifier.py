class Amplifier:
    def __init__(self, serial_number, model_string, manufacturer, next_maintenance, sampling_rate, gain):
        self.serial_number = serial_number
        self.model_string = model_string
        self.manufacturer = manufacturer
        self.next_maintenance = next_maintenance
        self.sampling_rate = sampling_rate
        self.gain = gain
        self.sensors = []
        self.is_on = False

    def set_gain(self, gain):
        if 1 <= gain <= 100:
            self.gain = gain
        else:
            raise ValueError("Gain level must be between 1 and 100 (including)")

    def set_sampling_rate(self, sampling_rate):
        if sampling_rate in [256, 512, 1024]:
            self.sampling_rate = sampling_rate
        else:
            raise ValueError("Sampling rate is typically 256, 512, or 1024 Hz")

    def power_on(self):
        self.is_on = True

    def power_off(self):
        self.is_on = False

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def remove_sensor(self, sensor):
        self.sensors.remove(sensor)

    def __str__(self):
            status = "On" if self.is_on else "Off"
            return (f"Amplifier {self.serial_number} - Model: {self.model_string}, "
                    f"Manufacturer: {self.manufacturer}, Next Maintenance: {self.next_maintenance}, "
                    f"Sampling Rate: {self.sampling_rate} Hz, Gain: {self.gain}, "
                    f"Status: {status}, "
                    f"Sensors: {[sensor.serial_number for sensor in self.sensors]}")