from amplifier import Amplifier
from control_system import EEGControlSystem
from sensor import Sensor

def main():
    """
    Main control system interface for managing amplifiers and sensors.
    
    This function provides an interactive menu for users to perform the following actions:
    1. Add a new amplifier with specified properties like serial number, model, manufacturer, sampling rate, and gain.
    2. Remove an existing amplifier by its serial number.
    3. List all amplifiers currently stored in the system, showing their details and status.
    4. Set the gain of an amplifier to a specified value within the allowed range.
    5. Set the sampling rate of an amplifier to one of the predefined values (256, 512, or 1024 Hz).
    6. Toggle the power state (on/off) of an amplifier.
    7. Search for amplifiers based on serial number, model string, or manufacturer.
    8. Create and add a new sensor to the system, specifying its serial number, model, manufacturer, maintenance date, and position on the scalp.
    9. Add an existing sensor to an amplifier by their serial numbers.
    10. Remove a sensor from an amplifier.
    11. Update the next maintenance date of either an amplifier or a sensor.
    12. Exit the system, saving the current state of amplifiers and sensors to a file.
    """
    control_system = EEGControlSystem()
    # Load the state on startup
    control_system.load_state()

    while True:
        print("1. Add Amplifier")
        print("2. Remove Amplifier")
        print("3. List Amplifiers")
        print("4. Set Gain")
        print("5. Set Sampling Rate")
        print("6. Power On/Off Amplifier")
        print("7. Search Amplifier")
        print("8. Create Sensor")
        print("9. Add Sensor to Amplifier")
        print("10. Remove Sensor from Amplifier")
        print("11. Update Maintenance Date")
        print("12. Exit from the System")
        choice = input("Please enter your choice: ")

        if choice == "1":
            # Add a new amplifier
            serial_number = input("Enter serial number: ")
            model_string = input("Enter model string: ")
            manufacturer = input("Enter manufacturer: ")
            next_maintenance = input("Enter next maintenance date (DD-MM-YYYY): ")

            while True:
                try:
                    sampling_rate = int(input("Enter sampling rate (256, 512, or 1024 Hz): "))
                    if sampling_rate not in [256, 512, 1024]:
                        raise ValueError("Invalid sampling rate.")
                    break
                except ValueError as e:
                    print(e)

            while True:
                try:
                    gain = int(input("Enter gain level [1-100]: "))
                    if not 1 <= gain <= 100:
                        raise ValueError("Gain must be between 1 and 100 (including)")
                    break
                except ValueError as e:
                    print(e)

            amplifier = Amplifier(serial_number, model_string, manufacturer, next_maintenance, sampling_rate, gain)
            control_system.add_amplifier(amplifier)

        elif choice == "2":
            # Remove an amplifier
            serial_number = input("Enter serial number of the amplifier to remove: ")
            control_system.remove_amplifier(serial_number)

        elif choice == "3":
            # List all amplifiers
            amplifiers = control_system.list_amplifiers()
            for amp in amplifiers:
                print(amp)

        elif choice == "4":
            # Set gain for an amplifier
            serial_number = input("Enter serial number of the amplifier: ")
            amplifier = control_system.find_amplifier(serial_number)
            if amplifier:
                gain = int(input("Enter new gain [1-100]: "))
                try:
                    amplifier.set_gain(gain)
                    print(f"Gain set to {gain}")
                except ValueError as e:
                    print(e)
            else:
                print("Amplifier not found.")

        elif choice == "5":
            # Set sampling rate for an amplifier
            serial_number = input("Enter serial number of the amplifier: ")
            amplifier = control_system.find_amplifier(serial_number)
            if amplifier:
                sampling_rate = int(input("Enter new sampling rate (256, 512, 1024 Hz): "))
                try:
                    amplifier.set_sampling_rate(sampling_rate)
                    print(f"Sampling rate set to {sampling_rate}")
                except ValueError as e:
                    print(e)
            else:
                print("Amplifier not found.")

        elif choice == "6":
            # Power on/off an amplifier
            serial_number = input("Enter serial number of the amplifier: ")
            amplifier = control_system.find_amplifier(serial_number)
            if amplifier:
                if amplifier.is_on:
                    amplifier.power_off()
                    print("Amplifier powered off")
                else:
                    amplifier.power_on()
                    print("Amplifier powered on")
            else:
                print("Amplifier not found")

        elif choice == "7":
            # Search for an amplifier
            print("Search by:")
            print("1. Serial Number")
            print("2. Model String")
            print("3. Manufacturer")
            search_option = input("Enter the number corresponding to your choice: ")
            
            if search_option == "1":
                search_by = "serial_number"
            elif search_option == "2":
                search_by = "model_string"
            elif search_option == "3":
                search_by = "manufacturer"
            else:
                print("Invalid search option.")
                continue
            
            query = input(f"Enter {search_by} to search: ")
            results = control_system.search_amplifiers(query, search_by)
            if results:
                for amp in results:
                    print(amp)
            else:
                print("No amplifiers found.")

        elif choice == "8":
            # Create a new sensor
            serial_number = input("Enter sensor serial number: ")
            model_string = input("Enter sensor model string: ")
            manufacturer = input("Enter sensor manufacturer: ")
            next_maintenance = input("Enter sensor next maintenance date (DD-MM-YYYY): ")
            tag = input("Enter sensor position on the scalp (e.g., 'frontal', 'occipital'): ")

            sensor = Sensor(serial_number, model_string, manufacturer, next_maintenance, tag)
            control_system.add_sensor(sensor)

        elif choice == "9":
            # Add a sensor to an amplifier
            amplifier_serial = input("Enter amplifier serial number: ")
            sensor_serial = input("Enter sensor serial number: ")
            control_system.add_sensor_to_amplifier(amplifier_serial, sensor_serial)

        elif choice == "10":
            # Remove a sensor from an amplifier
            amplifier_serial = input("Enter amplifier serial number: ")
            sensor_serial = input("Enter sensor serial number: ")
            control_system.remove_sensor_from_amplifier(amplifier_serial, sensor_serial)

        elif choice == "11":
            # Update the maintenance date
            device_type = input("Update maintenance date for Amplifier or Sensor (A/S): ").lower()
            serial_number = input("Enter the serial number of the device: ")
            new_date = input("Enter the new maintenance date (DD-MM-YYYY): ")

            if device_type == "a":
                amplifier = control_system.find_amplifier(serial_number)
                if amplifier:
                    control_system.update_maintenance_date(amplifier, new_date)
                else:
                    print("Amplifier not found.")

            elif device_type == "s":
                sensor = control_system.find_sensor(serial_number)
                if sensor:
                    control_system.update_maintenance_date(sensor, new_date)
                else:
                    print("Sensor not found.")
            else:
                print("Invalid option. Please select 'A' for Amplifier or 'S' for Sensor.")
        
        elif choice == "12":
            print("Exiting and saving state...")
            control_system.save_state()  # Save state on exit
            break
        
        else:
            print("Invalid choice")

main()