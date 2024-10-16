class Sensor:
    """
    Represents a sensor in the EEG system, including its serial number, model, 
    manufacturer, next maintenance date, and position on the scalp (tag).

    Attributes:
        serial_number (str): The serial number of the sensor.
        model_string (str): The model of the sensor.
        manufacturer (str): The manufacturer of the sensor.
        next_maintenance (str): The date of the next maintenance in 'YYYY-MM-DD' format.
        tag (str): The position on the scalp (e.g., 'frontal', 'occipital').
    """
    def __init__(self, serial_number, model_string, manufacturer, next_maintenance, tag):
        self.serial_number = serial_number
        self.model_string = model_string
        self.manufacturer = manufacturer
        self.next_maintenance = next_maintenance
        self.tag = tag  # position on the scalp

    def __str__(self):
        return f"Sensor {self.serial_number} ({self.tag}) - Model: {self.model_string}, Manufacturer: {self.manufacturer}, Next Maintenance: {self.next_maintenance}"
