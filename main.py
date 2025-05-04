# Author: Biyoni Pietersz
# Date: 17/12/2024
# IIT Student ID: 20232487
# Westminster Student ID: 2120755

import csv  # Importing CSV files
import os  # Importing the os module to interact with the operating system

from gui import HistogramApp, MultiCSVProcessor


# Task A: Input Validation

def validate_input(prompt, min_val, max_val):
    """
    Validate user input within a specific range with comprehensive error handling.

    Args:
        prompt (str): The input prompt for the user
        min_val (int): Minimum allowed value
        max_val (int): Maximum allowed value

    Returns:
        int: A validated integer within the specified range
    """
    while True:
        try:
            # Strip whitespace and handle empty input
            user_input = input(prompt).strip()

            # Check for empty input
            if not user_input:
                print("Input cannot be empty.")
                continue

            # Attempt to convert input to integer
            value = int(user_input)

            # Check if value is within the specified range
            if value < min_val or value > max_val:
                print(f"Out of range - values must be in the range {min_val} and {max_val}.")
            else:
                return value

        except ValueError:
            # Handle non-integer inputs
            print("Integer required.")


def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    - Handles leap year considerations

    Returns:
        tuple: Validated day, month, and year
    """
    while True:
        # Validate day input
        day = validate_input("Please enter the day of the survey in the format DD: ", 1, 31)

        # Validate month input
        month = validate_input("Please enter the month of the survey in the format MM: ", 1, 12)

        # Validate year input
        year = validate_input("Please enter the year of the survey in the format YYYY: ", 2000, 2024)

        # Define the maximum days in each month
        days_in_month = {
            1: 31, 2: 28, 3: 31, 4: 30,
            5: 31, 6: 30, 7: 31, 8: 31,
            9: 30, 10: 31, 11: 30, 12: 31
        }

        # Check for leap year and adjust February's days
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            print("Its a leap year")
            days_in_month[2] = 29

        # Validate the day against the month
        if day > days_in_month[month]:
            print(f"Invalid day for month {month}. Maximum days are {days_in_month[month]}.")
            continue  # Restart the input process

        # If all validations pass, return the date
        return day, month, year


def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    - Case-insensitive
    - Handles whitespace

    Returns:
        bool: True if user wants to continue, False otherwise
    """
    while True:
        try:
            # Get input, strip whitespace, and convert to lowercase
            user_input = input("\nProcess another file? (y/n): ").strip().lower()

            # Check for empty input
            if not user_input:
                print("Input cannot be empty.")
                continue

            # Validate input
            if user_input in ['y', 'n']:
                return user_input == 'y'

            # Handle invalid inputs
            print("Invalid input. Enter 'y' for yes or 'n' for no.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# Task B: Processed Outcomes


# Process traffic data from the CSV file
def process_csv_data(file_path, day, month, year):
    """
    Reads and processes data from the CSV file for a specific date.
    Calculates traffic-related statistics and returns a dictionary of outcomes.
    """

    # initialize the dictionary for outcomes
    outcomes = {
        "Total Vehicles": 0,
        "Total Trucks": 0,
        "Total Electric Vehicles": 0,
        "Two-Wheeled Vehicles": 0,
        "Buses North": 0,
        "Straight Through": 0,
        "Truck Percentage": 0,
        "Over Speed Limit": 0,
        "Elm Ave Rabbit Road": 0,
        "Hanley Highway Westway": 0,
        "Scooter Percentage": 0,
        "Highest Hourly Count": 0,
        "Most Vehicles Hour": "",
        "Rain Hours": 0,
        "Date": f"{day:02d}{month:02d}{year}",
        "Data File": os.path.basename(file_path)
    }

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")  # Notify user if file is missing
        return None

    # Initialize counters for specific statistic
    total_vehicles = 0
    total_trucks = 0
    total_electric_vehicles = 0
    two_wheeled_vehicles = 0
    buses_north = 0
    straight_through = 0
    over_speed_limit = 0
    elm_ave_vehicles = 0
    hanley_highway_vehicles = 0
    scooters = 0
    rainy_hours = set()
    hourly_bicycles = set()
    hanley_hourly_counts = {}
    rabbit_rd_hourly_counts = {}
    total_bicycle_count = 0

    try:
        # Open the file and read row by row
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)  # Read rows as dictionaries

            for row in reader:
                # Extract relevant data from each row
                vehicle_type = row["VehicleType"]
                time_of_day = row["timeOfDay"]
                speed_limit = int(row["JunctionSpeedLimit"])
                vehicle_speed = int(row["VehicleSpeed"])
                is_electric = row["electricHybrid"] == "True"
                junction_name = row["JunctionName"]
                weather_conditions = row["Weather_Conditions"]
                travel_in = row["travel_Direction_in"]
                travel_out = row["travel_Direction_out"]

                # Increment total vehicles for every row
                total_vehicles += 1

                # Count vehicles at "Elm Avenue/Rabbit Road"
                if junction_name == "Elm Avenue/Rabbit Road":
                    elm_ave_vehicles += 1

                # Count vehicles at "Hanley Highway/Westway"
                if junction_name == "Hanley Highway/Westway":
                    hanley_highway_vehicles += 1

                # Count trucks
                if vehicle_type == "Truck":
                    total_trucks += 1

                # Count electric vehicles
                if is_electric:
                    total_electric_vehicles += 1

                # Count two-wheeled vehicles (Bicycle, Motorcycle, Scooter)
                if vehicle_type in ["Bicycle", "Motorcycle", "Scooter"]:
                    two_wheeled_vehicles += 1

                # Count buses heading North from "Elm Avenue/Rabbit Road"
                if junction_name == "Elm Avenue/Rabbit Road" and vehicle_type == "Buss" and travel_out == "N":
                    buses_north += 1

                # Count vehicles that passed straight through without turning
                if travel_in == travel_out:
                    straight_through += 1

                # Count vehicles exceeding the speed limit
                if vehicle_speed > speed_limit:
                    over_speed_limit += 1

                # Count scooters at "Elm Avenue/Rabbit Road"
                if vehicle_type == "Scooter" and junction_name == "Elm Avenue/Rabbit Road":
                    scooters += 1

                # Count hourly vehicles at "Hanley Highway/Westway"
                if junction_name == "Hanley Highway/Westway":
                    hour = time_of_day.split(":")[0]
                    if hour not in hanley_hourly_counts:
                        hanley_hourly_counts[hour] = 0
                    hanley_hourly_counts[hour] += 1

                # Count hourly vehicles at "Elm Avenue/Rabbit Road"
                if junction_name == "Elm Avenue/Rabbit Road":
                    hour = time_of_day.split(":")[0]
                    if hour not in rabbit_rd_hourly_counts:
                        rabbit_rd_hourly_counts[hour] = 0
                    rabbit_rd_hourly_counts[hour] += 1

                    # Record hourly bicycle counts
                    if vehicle_type == "Bicycle":
                        hour = time_of_day.split(":")[0]  # Extract the hour
                        hourly_bicycles.add(hour)  # Track unique hours bicycles were recorded
                        total_bicycle_count += 1  # Increment total bicycle count

                    # Count rainy hours
                    date = row["Date"]
                    time_of_day = row["timeOfDay"]
                    if weather_conditions == "Light Rain" or weather_conditions == "Heavy Rain":
                        # Extract hour from the time_of_day
                        hour = time_of_day.split(":")[0]
                        # Create a unique key for (date, hour)
                        rainy_hours.add((date, hour))
            total_rainy_hours = len(rainy_hours)

        # Update calculated values into outcomes dictionary
        outcomes.update({
            "Total Vehicles": total_vehicles,
            "Total Trucks": total_trucks,
            "Total Electric Vehicles": total_electric_vehicles,
            "Two-Wheeled Vehicles": two_wheeled_vehicles,
            "Buses North": buses_north,
            "Straight Through": straight_through,
            "Over Speed Limit": over_speed_limit,
            "Elm Ave Rabbit Road": elm_ave_vehicles,
            "Hanley Highway Westway": hanley_highway_vehicles,
            "Truck Percentage": round((total_trucks / total_vehicles) * 100) if total_vehicles else 0,
            "Rain Hours": total_rainy_hours,
        })

        # Calculate the total number of unique hours for the date
        unique_hours_in_day = len(set(range(0, 24)))  # 24 hours in a day
        total_hours = unique_hours_in_day

        average_bicycles_per_hour = round(total_bicycle_count / total_hours) if total_hours > 0 else 0
        outcomes["Average Bicycles Per Hour"] = average_bicycles_per_hour

        # Calculate scooter percentage at "Elm Avenue/Rabbit Road"
        if elm_ave_vehicles > 0:  # Check if there are any vehicles recorded at "Elm Avenue/Rabbit Road"
            scooter_percentage = (
                                             scooters / elm_ave_vehicles) * 100  # Calculate the percentage of scooters relative to total vehicles at this location
            outcomes["Scooter Percentage"] = int(
                scooter_percentage)  # Store the percentage in the outcomes dictionary, converting it to an integer
        else:
            outcomes["Scooter Percentage"] = 0  # If no vehicles are recorded, set scooter percentage to 0

        # Calculate highest hourly vehicle count at "Hanley Highway/Westway"
        if hanley_hourly_counts:  # Check if there are hourly counts recorded for "Hanley Highway/Westway"
            highest_hourly_count = max(
                hanley_hourly_counts.values())  # Find the highest hourly vehicle count at this location
            outcomes[
                "Highest Hourly Count"] = highest_hourly_count  # Store the highest hourly count in the outcomes dictionary
            most_vehicles_hours = [hour for hour, count in hanley_hourly_counts.items() if
                                   count == highest_hourly_count]  # Identify the hour(s) during which this highest count occurred
            # Format the hours into a human-readable string and store in the outcomes dictionary
            outcomes["Most Vehicles Hour"] = " and ".join(
                [f"Between {hour}:00 and {int(hour) + 1}:00" for hour in most_vehicles_hours])

    except Exception as e:  # Handle any exceptions that occur during file processing
        print(f"Error processing file: {e}")  # Print an error message

    return outcomes  # Return the processed data


def display_outcomes(outcomes):
    """
    Print the outcomes in the specified format.

    Args:
    outcomes (dict): Dictionary of traffic metrics
    """
    if not outcomes:
        # Check if outcomes are empty
        print("No data to display.")
        return

    # Print each outcome in a formatted manner
    print("\n***************************************************************")
    print(f"data file selected is {outcomes['Data File']}")
    print("***************************************************************\n")
    print(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}")
    print(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}")
    print(f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}")
    print(f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}")
    print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Buses North']}")
    print(
        f"The total number of Vehicles through both junctions not turning left or right is {outcomes['Straight Through']}")
    print(
        f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Truck Percentage']}%.")
    print(f"The average number of Bikes per hour for this date is {outcomes['Average Bicycles Per Hour']}")
    print(
        f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['Over Speed Limit']}")
    print(
        f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Ave Rabbit Road']}")
    print(
        f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Highway Westway']}")
    print(f"{outcomes['Scooter Percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Highest Hourly Count']}")
    print(f"The most vehicles through Hanley Highway/Westway were recorded {outcomes['Most Vehicles Hour']}")
    print(f"The number of hours of rain for this date is {outcomes['Rain Hours']}")
    # End of report formatting
    print("\n***************************************************************\n")


# Task C: Save Results to Text File


def save_results_to_file(outcomes_list):
    """
    Save the processed traffic outcomes to a text file.
    Appends results if multiple datasets are processed in one session.
    """
    file_name = "results.txt"  # Define the output file name
    print("File saved as results.txt")
    try:
        # Attempt to open the file in append mode ('a') to add new results without overwriting existing data
        with open(file_name, "a") as file:
            # Iterate through each outcome dictionary in the outcomes_list
            for outcomes in outcomes_list:
                # Write each outcome to the file
                file.write(f"Data file selected is {outcomes['Data File']}\n")
                file.write(f"\nThe total number of vehicles recorded for this date is {outcomes['Total Vehicles']}\n")
                file.write(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}\n")
                file.write(
                    f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}\n")
                file.write(
                    f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}\n")
                file.write(
                    f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Buses North']}\n")
                file.write(
                    f"The total number of Vehicles through both junctions not turning left or right is {outcomes['Straight Through']}\n")
                file.write(
                    f"The percentage of total vehicles recorded that are trucks for this date is {outcomes['Truck Percentage']}%\n")
                file.write(
                    f"The average number of Bikes per hour for this date is {outcomes['Average Bicycles Per Hour']}\n")
                file.write(
                    f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['Over Speed Limit']}\n")
                file.write(
                    f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Ave Rabbit Road']}\n")
                file.write(
                    f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Highway Westway']}\n")
                file.write(
                    f"{outcomes['Scooter Percentage']}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters\n")
                file.write(
                    f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Highest Hourly Count']}\n")
                file.write(
                    f"The most vehicles through Hanley Highway/Westway were recorded between {outcomes['Most Vehicles Hour']}\n")
                file.write(f"The number of hours of rain for this date is {outcomes['Rain Hours']}\n")
                file.write("\n***************************************************************\n")

    except Exception as e:
        # Handle errors during file writing
        print(f"Error saving results: {e}")


# Main Function
def main():
    print("*********************************************\n"
          "\tTraffic Data Analysis Program\n"
          "*********************************************\n")

    outcomes_list = []  # Store results for multiple files
    processor = MultiCSVProcessor()  # Object to handle multiple CSV files

    while True:
        # Get the survey date from the user with error handling
        try:
            day, month, year = validate_date_input()
        except ValueError as e:
            print(f"Invalid date input: {e}. Please try again.")
            continue

        # Generate the expected CSV file name
        file_name = f"traffic_data{day:02}{month:02}{year}.csv"

        try:
            # Load CSV file using MultiCSVProcessor
            processor.load_csv_file(file_name)

            # Task B: Process CSV Data
            try:
                outcomes = process_csv_data(file_name, day, month, year)
                if outcomes:
                    # Add outcomes to the list and display them
                    outcomes_list.append(outcomes)
                    display_outcomes(outcomes)
            except Exception as e:
                print(f"Error processing CSV data: {e}. Skipping this file.")
                continue

            # Task D: Display Histogram using HistogramApp
            try:
                app = HistogramApp(processor.current_data, f"{day:02d}/{month:02d}/{year}")
                app.run()
            except Exception as e:
                print(f"Error displaying histogram: {e}. Skipping this file.")
                continue

        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.\n")
            continue

        # Check if the user wants to process another file
        try:
            if not validate_continue_input():
                break
        except ValueError:
            print("Invalid input. Please enter 'Y' for yes or 'N' for no.")
            continue

    # Save results with error handling
    try:
        save_results_to_file(outcomes_list)
    except IOError as e:
        print(f"Error saving results to file: {e}. Please check your file permissions and try again.")



# Entry point of the program
if __name__ == "__main__":
    # Call the main function to start the program
    main()
