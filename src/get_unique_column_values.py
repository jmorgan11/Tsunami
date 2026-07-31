"""Get unique values from a column in all the CSVs in a folder."""
import pandas as pd
from pathlib import Path
import os
import math

# Location of folders with CSV's to check.
csv_folder_path = [
    r"C:\GIS\Tsunami\Scripts\data",
]

# State's in Scope of Work
states_to_check = ["CA", "OR", "WA", "AK", "HI"]

# Full list
full_list = []

# Field to look at
field = 'NUM_STORIES'

for csv_folder in csv_folder_path:

    # Get a list of files in the folder
    folder_path = Path(csv_folder)
    files = [f.name for f in folder_path.iterdir() if f.is_file()]

    for file in files:
        if file.endswith(".csv"):
            if any(state in file for state in states_to_check):
                full_path = os.path.join(folder_path, file)
                print(f"{full_path}")

                df = pd.read_csv(full_path)

                try:
                    unique_values = df[field].unique()
                    full_list.extend(unique_values.tolist())
                    full_list = list(set(full_list))

                    full_list = [x for x in full_list if not math.isnan(x)]
                except KeyError:
                    print(f"\t...{field} does not exist.")

    print("----------------------------------------")
    print(f"{csv_folder} - field: {field}")
##    print(f"\tFull unique value list for {field}:")
##    for val in sorted(full_list):
##        print("\t\t", val)
    sorted_full_list = sorted(full_list)
    print(f"\tLow: {sorted_full_list[0]}")
    print(f"\tHigh: {sorted_full_list[-1]}")
