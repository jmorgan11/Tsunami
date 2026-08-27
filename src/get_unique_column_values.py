"""Get unique values from a column in all the CSVs in a folder."""
from pathlib import Path
import os
import pandas as pd

# Location of folders with CSV's to check.
csv_folder_path = [
    "C:\\GIS\\Tsunami\\Scripts\data\\TSU_Uncorrelated_Data",
]

# State's in Scope of Work
states_to_check = ["CA", "OR", "WA", "AK", "HI"]

# Full list
full_list = []

# Fields available
"""
Field                  Type         Min             Min             Unique
------------------------------------------------------------------------------------
accntnum               object   1-AK00000001    1-WA01978993
location               object     AK00000001      WA01978993
BLDG_DED                int64              0          10,000
BLDG_LIMIT              int64              0      81,459,690
CNT_DED                 int64              0          10,000
CNT_LIMIT               int64              0      10,143,036
STATE                  object             AK              WA       AK, HI, OR, WA
POSTCODE              float64        89421.0         98303.0
COUNTRY                object             US              US                   US
LON                   float64    -176.654683      -116.769897
LAT                   float64      18.970043        71.307217
BLDG_VALUE              int64              0      314,608,860
CNT_VALUE               int64              0      130,189,140
CONSTR_CODE             int64              1                6        1, 2, 4, 5, 6
NUM_STORIES             int64              1               40        1 through 40
YEAR_BUILT              int64           1900             2017        1900 through 2017
foundationtype          int64              2                9        2, 4, 6, 7, 8, 9
BasementFinishType      int64              0                1
FIRST_FLOOR_ELEV        int64              0               10        0 through 10
BASE_FLOOD_ELEV        object              1              999        Unknown values exists
elev_ft               float64           -7.6         13,367.8
BLDG_TYPE              object              -                -        'MOBILE_MANUFACTURED_HOME', 'NON_RESIDENTIAL_BUILDING', 
                                                                     'ONE_TO_FOUR_FAMILY_BUILDING', 'OTHER_RESIDENTIAL_BUILDING', 
                                                                     'RESIDENTIAL_CONDOMINIUM_BUILDING', 'RESIDENTIAL_UNIT'
NUM_UNITS               int64              1              400        1 through 400
UNITS_PER_FLOOR       float64            1.0             10.0        1.0 through 10.0
"""

# Field to look at
field = 'UNITS_PER_FLOOR'

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

                except KeyError:
                    print(f"\t...{field} does not exist.")

    print("----------------------------------------")
    print(f"{csv_folder} - field: {field}")
    print(f"\tFull unique value list for {field}:")
    sorted_full_list = sorted(full_list)
    print(sorted_full_list)
    print(f"\tLow: {sorted_full_list[0]}")
    print(f"\tHigh: {sorted_full_list[-1]}")
