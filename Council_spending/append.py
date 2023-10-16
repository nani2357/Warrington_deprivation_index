import pandas as pd
import os
from pathlib import Path
from datetime import datetime

# Function to convert year and month to a datetime object
def convert_to_date(year, month):
    formats = ['%Y %B', '%Y %b']
    for fmt in formats:
        try:
            return datetime.strptime(f'{year} {month}', fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot convert {year} {month} into datetime.")

# The folder where your processed files are stored
processed_folder = Path('D:\\Warrington_council\\Warrington_deprivation_index\\Council_spending\\data_python')

# Creating an empty list to hold DataFrames
dfs = []

# Creating a log file to write errors
log_file = processed_folder / "log.txt"
with open(log_file, "w") as log:
    # Adding each file in the processed folder to the dfs list
    for file in os.listdir(processed_folder):
        try:
            file_path = processed_folder / file
            if file.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                log.write(f"Skipped {file} as it is not a CSV or Excel file.\n")
                continue
            
            dfs.append(df)
            log.write(f"Processed {file} successfully.\n")
        except Exception as e:
            log.write(f"Could not process {file} due to error: {str(e)}\n")

# Concatenating all DataFrames in the dfs list into a single DataFrame
try:
    all_data = pd.concat(dfs, ignore_index=True)

    # Converting the 'Year' and 'Month' columns into datetime format and creating a new 'Date' column
    all_data['Date'] = all_data.apply(lambda x: convert_to_date(x['Year'], x['Month']), axis=1)

    # Sorting the DataFrame by the 'Date' column
    all_data = all_data.sort_values(by='Date')

    # Dropping the 'Date' column if it's not needed
    all_data.drop(columns=['Date'], inplace=True)

    # Saving the sorted DataFrame to a new file
    all_data.to_csv(processed_folder / 'all_data_sorted.csv', index=False)

    print("Data concatenated and sorted successfully.")
except Exception as e:
    with open(log_file, "a") as log:
        log.write(f"Failed to concatenate or sort data due to error: {str(e)}\n")
