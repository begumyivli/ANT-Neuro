class Sensor:
    def __init__(self, serial_number, model_string, manufacturer, next_maintenance, tag):
        self.serial_number = serial_number
        self.model_string = model_string
        self.manufacturer = manufacturer
        self.next_maintenance = next_maintenance
        self.tag = tag  # position on the scalp

    def __str__(self):
        return f"Sensor {self.serial_number} ({self.tag}) - Model: {self.model_string}, Manufacturer: {self.manufacturer}, Next Maintenance: {self.next_maintenance}"
