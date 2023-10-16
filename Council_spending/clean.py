import pandas as pd
import os
import re
from pathlib import Path

# The folder containing your files
input_folder = Path('D:\\Warrington_council\\Warrington_deprivation_index\\Council_spending\\raw_data')
# The folder where you want to save the updated files, it will be created if doesn't exist
output_folder = Path('D:\\Warrington_council\\Warrington_deprivation_index\\Council_spending\\data_python')
output_folder.mkdir(parents=True, exist_ok=True)

# Updated regex pattern to be case insensitive and handle different separators and formats
pattern = re.compile(r'([A-Za-z]+)[-_ ](\d{4})', re.IGNORECASE)

def read_file(file_path, file_extension):
    try:
        if file_extension == '.csv':
            return pd.read_csv(file_path, encoding='utf-8')
        elif file_extension == '.xlsx':
            return pd.read_excel(file_path)
    except UnicodeDecodeError:
        if file_extension == '.csv':
            return pd.read_csv(file_path, encoding='ISO-8859-1')

for file in os.listdir(input_folder):
    file_extension = os.path.splitext(file)[1]
    if file_extension in ['.csv', '.xlsx']:
        print(f"Processing {file}...")
        match = pattern.search(file)
        if match:
            month, year = match.groups()
            file_path = input_folder / file
            df = read_file(file_path, file_extension)
            
            if df is not None:
                # Adding the year and month columns
                df['Year'] = year
                df['Month'] = month.title()  # Convert month to title case for consistency
                
                # Saving the updated DataFrame to a new file in the output folder
                output_file = output_folder / file
                if file_extension == '.csv':
                    df.to_csv(output_file, index=False, encoding='utf-8')
                elif file_extension == '.xlsx':
                    df.to_excel(output_file, index=False)
                print(f"Processed {file} successfully.")
            else:
                print(f"Could not read {file}.")
        else:
            print(f"Skipped {file} because it did not match the pattern.")
    else:
        print(f"Skipped {file} because it is not a CSV or Excel file.")

print("Processing complete.")
