import csv
import tkinter as tk


# Task D: Histogram Display using graphics.py
class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.root.title(f"Histogram - {self.date}")
        self.canvas = tk.Canvas(self.root, width=900, height=620, bg="white")
        self.canvas.pack()

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """

        self.canvas.create_text(
            400, 40, text=f"Histogram of Vehicle Frequency per Hour ({self.date})", font=("Poppins", 16)
        )

        # X-axis Label
        self.canvas.create_text(
            400, 580, text="Hours 00:00 to 24:00", font=("Poppins", 12)
        )

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        hourly_data = {hour: [0, 0] for hour in range(24)}

        for record in self.traffic_data:
            hour = int(record['timeOfDay'].split(":")[0])
            if record['JunctionName'] == 'Elm Avenue/Rabbit Road':
                hourly_data[hour][0] += 1
            elif record['JunctionName'] == 'Hanley Highway/Westway':
                hourly_data[hour][1] += 1

        max_traffic = max(max(counts) for counts in hourly_data.values())
        scaling_factor = 450 / max_traffic if max_traffic > 0 else 1

        for hour, (elm_count, hanley_count) in hourly_data.items():
            x0 = 60 + hour * 30
            elm_height = elm_count * scaling_factor
            hanley_height = hanley_count * scaling_factor

            # Draw Elm Avenue bar
            self.canvas.create_rectangle(x0, 550 - elm_height, x0 + 10, 550, fill="#4bc949", outline="#4bc949")
            # Display value on top of Elm Avenue bar
            self.canvas.create_text(x0 + 5, 550 - elm_height - 10, text=str(elm_count), font=("Arial", 8),
                                    fill="green")
            # Draw Hanley Highway bar
            self.canvas.create_rectangle(x0 + 15, 550 - hanley_height, x0 + 25, 550, fill="#f9969b", outline="#f9969b")
            # Display value on top of Hanley Highway bar
            self.canvas.create_text(x0 + 20, 550 - hanley_height - 10, text=str(hanley_count), font=("Arial", 8),
                                    fill="red")

            # Label the hour below the bars
            self.canvas.create_text(x0 + 14, 560, text=f"{hour:02d}", font=("Arial", 8))

    def add_legend(self):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        self.canvas.create_rectangle(650, 100, 670, 120, fill="#4bc949", outline="#4bc949")
        self.canvas.create_text(700, 110, text="Elm Avenue/Rabbit Road", anchor="w", font=("Arial", 10))
        self.canvas.create_rectangle(650, 130, 670, 150, fill="#f9969b", outline="#f9969b")
        self.canvas.create_text(700, 140, text="Hanley Highway/Westway", anchor="w", font=("Arial", 10))

    def run(self):
        """
        Runs the Tkinter main loop to display the histogram.
        """
        self.setup_window()
        self.draw_histogram()
        self.add_legend()
        self.root.mainloop()


# Task E: Code Loops to Handle Multiple CSV Files
class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            self.current_data = list(reader)

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            file_path = input("Please enter the CSV file path: ").strip()
            try:
                self.load_csv_file(file_path)
                break
            except FileNotFoundError:
                print("File not found. Please try again.")

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        while True:
            self.clear_previous_data()
            self.handle_user_interaction()

            date = input("Please enter the date for the histogram (DD/MM/YYYY): ").strip()
            app = HistogramApp(self.current_data, date)
            app.run()

            continue_input = input("Do you want to process another file? (Y/N): ").strip().upper()
            if continue_input == 'N':
                break
