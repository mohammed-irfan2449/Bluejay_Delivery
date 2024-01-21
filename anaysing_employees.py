import pandas as pd
from datetime import timedelta

def parse_time(time_str):
    return pd.to_datetime(time_str, format='%m/%d/%Y %I:%M %p', errors='coerce')

def analyze_employee_data(file_path):
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        for employee in set(df['Employee Name']):
            employee_entries = df[df['Employee Name'] == employee]
            consecutive_days = 1
            previous_end_time = parse_time(employee_entries.iloc[0]['Time Out'])
            total_hours_in_shift = 0

            for index, entry in employee_entries.iloc[1:].iterrows():
                start_time = parse_time(entry['Time'])
                end_time = parse_time(entry['Time Out'])

                # Check for consecutive days
                if (start_time - previous_end_time).days == 1:
                    consecutive_days += 1
                else:
                    consecutive_days = 1

                # Check for less than 10 hours between shifts
                if (start_time - previous_end_time) < timedelta(hours=10) and (start_time - previous_end_time) > timedelta(hours=1):
                    print(f"Employee: {employee}, Position: {entry['Position ID']}, Less than 10 hours between shifts")

                # Check for more than 14 hours in a single shift
                shift_duration = end_time - start_time
                if shift_duration > timedelta(hours=14):
                    print(f"Employee: {employee}, Position: {entry['Position ID']}, More than 14 hours in a single shift")

                previous_end_time = end_time
                total_hours_in_shift += shift_duration.total_seconds() / 3600

            # Check for 7 consecutive days
            if consecutive_days >= 7:
                print(f"Employee: {employee}, Position: {employee_entries.iloc[0]['Position ID']}, Worked for 7 consecutive days")

            # Check for less than 10 hours in total for the pay cycle
            if total_hours_in_shift < 10:
                print(f"Employee: {employee}, Position: {employee_entries.iloc[0]['Position ID']}, Worked less than 10 hours in total for the pay cycle")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = r"C:\Users\fazal khairu\Desktop\Assignment_Timecard.xlsx - Sheet1.csv"  
    analyze_employee_data(file_path)





