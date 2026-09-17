"""
Filename: populate_eq_design_level_hawaii.py
Purpose: Populate Earthquake Design Level (EqDesignLe) field for Hawaii.
Author: Jesse Morgan
Date: 9/17/2026
Updates: None

Note: Scope of work only includes Hawaii.
"""
import os
import sys
from pathlib import Path
import arcpy

def process_hawaii_county(square_feet: float, year_built: int,
                          occupancy_type: str, number_stories: int):
    """
    Process points for Hawaii County

    Args:
        square_feet (float) - building square footage
        year_built (int) - year the building was constructed
        occupancy_type (str) - occupancy type of the building
        number_of_stories (int) - number of floors

    Returns:
        table name to use
    """
    table_name = None

    if year_built < 2013:
        table_name = "pre-IBC"

    elif occupancy_type in ("RES1", "RES3A"):
        if square_feet <= 1500:
            table_name =  "IRC 2006 W1/RES1 Design Level, <=1500 SQFT"
        else:
            table_name = "IRC 2006 W1/RES1 Design Level, > 1500 SQFT"

    elif number_stories < 4:
        table_name = "IBC 2006, Low-Rise Design Level"

    elif number_stories > 4:
        table_name = "IBC 2006, Mid-Rise/High-Rise Design Level"

    return table_name

def process_honolulu_county(square_feet: float, year_built: int,
                            occupancy_type: str, number_stories: int):
    """
    Process points for Honolulu County

    Args:
        square_feet (float) - building square footage
        year_built (int) - year the building was constructed
        occupancy_type (str) - occupancy type of the building
        number_of_stories (int) - number of floors

    Returns:
        table name to use
    """
    table_name = None

    if year_built < 2008:
        table_name = "pre-IBC"

    elif occupancy_type in ("RES1", "RES3A"):
        if square_feet <= 1500:
            if year_built <= 2012:
                table_name =  "IRC 2003 W1/RES1 Design Level, <=1500 SQFT"
            else:
                table_name = "IRC 2006 W1/RES1 Design Level, <=1500 SQFT"
        elif year_built <= 2012:
            table_name = "IRC 2003 W1/RES1 Design Level, > 1500 SQFT"
        else:
            table_name = "IRC 2006 W1/RES1 Design Level, > 1500 SQFT"

    elif number_stories < 4:
        if year_built <= 2012:
            table_name = "IBC 2003, Low-Rise Design Level"
        else:
            table_name = "IBC 2006, Low-Rise Design Level"

    elif number_stories > 4:
        if year_built <= 2012:
            table_name = "IBC 2003, Mid-Rise/High-Rise Design Level"
        else:
            table_name = "IBC 2006, Mid-Rise/High-Rise Design Level"

    return table_name

def process_maui_county(square_feet: float, year_built: int,
                        occupancy_type: str, number_stories: int):
    """
    Process points for Maui County

    Args:
        square_feet (float) - building square footage
        year_built (int) - year the building was constructed
        occupancy_type (str) - occupancy type of the building
        number_of_stories (int) - number of floors

    Returns:
        table name to use
    """
    table_name = None

    if year_built < 2013:
        table_name = "pre-IBC"

    elif occupancy_type in ("RES1", "RES3A"):
        if square_feet <= 1500:
            table_name =  "IRC 2006 W1/RES1 Design Level, <=1500 SQFT"
        else:
            table_name = "IRC 2006 W1/RES1 Design Level, > 1500 SQFT"

    elif number_stories < 4:
        table_name = "IBC 2006, Low-Rise Design Level"

    elif number_stories > 4:
        table_name = "IBC 2006, Mid-Rise/High-Rise Design Level"

    return table_name

def main(in_fc):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class to process.

    Returns:
        None
    """
    fields = ["Tract", "CountyName", "AreaSqft", "YEAR_BUILT", "Occupancy_Type", "NUM_STORIES"]
    with arcpy.da.SearchCursor(in_table=in_fc, field_names=fields) as cursor:
        for row in cursor:
            census_tract = row[0]
            county_name = row[1]
            square_feet = row[2]
            year_built = row[3]
            occupancy_type = row[4]
            number_stories = row[5]

            # TODO: Add logic for COM6, GOV2, EDU1 and EDU2
            if occupancy_type in ("COM6", "GOV2", "EDU1", "EDU2"):
                print(f"********Occupancy Type {occupancy_type} found.  NEED TO UPDATE!***********")

            if county_name == "Hawaii":
                table_name = process_hawaii_county(square_feet, year_built,
                                                   occupancy_type, number_stories)

            elif county_name == "Honolulu":
                table_name = process_honolulu_county(square_feet, year_built,
                                                   occupancy_type, number_stories)

            elif county_name in ("Maui", "Kalawao"):
                table_name = process_maui_county(square_feet, year_built,
                                                 occupancy_type, number_stories)                

                print(f"##TESTING###: {table_name} -> occ_typ: {occupancy_type}, year: {year_built}, stories: {number_stories}, sqft: {square_feet}")


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "hi_uni.gdb\\hi_uni_points")

    main(in_fc=feature_class)