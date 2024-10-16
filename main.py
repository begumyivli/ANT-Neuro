from amplifier import Amplifier
from control_system import EEGControlSystem
from sensor import Sensor

def main():
    control_system = EEGControlSystem()
    while True:
        print("1. Add Amplifier")
        print("2. Remove Amplifier")
        print("3. List Amplifiers")
        print("4. Set Gain")
        print("5. Set Sampling Rate")
        print("6. Power On/Off Amplifier")
        print("7. Search Amplifier")
        print("8. Add Sensor to Amplifier")
        print("9. Remove Sensor from Amplifier")
        choice = input("Please enter your choice: ")

        if choice == "1":
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
            serial_number = input("Enter serial number of the amplifier to remove: ")
            control_system.remove_amplifier(serial_number)

        elif choice == "3":
            amplifiers = control_system.list_amplifiers()
            for amp in amplifiers:
                print(amp)

        elif choice == "4":
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
            # Add a sensor to an amplifier
            amplifier_serial = input("Enter amplifier serial number: ")
            sensor_serial = input("Enter sensor serial number: ")
            model_string = input("Enter sensor model string: ")
            manufacturer = input("Enter sensor manufacturer: ")
            next_maintenance = input("Enter sensor next maintenance date (DD-MM-YYYY): ")
            tag = input("Enter sensor position on the scalp (e.g., 'frontal', 'occipital'): ")
            sensor = Sensor(sensor_serial, model_string, manufacturer, next_maintenance, tag)
            control_system.add_sensor_to_amplifier(amplifier_serial, sensor)

        elif choice == "9":
            # Remove a sensor from an amplifier
            amplifier_serial = input("Enter amplifier serial number: ")
            sensor_serial = input("Enter sensor serial number: ")
            control_system.remove_sensor_from_amplifier(amplifier_serial, sensor_serial)
        
        else:
            print("Invalid choice")

main()