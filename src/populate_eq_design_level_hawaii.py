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
from seismic import SEISMIC_CODES


def process_hawaii_county(
    square_feet: float, year_built: int, occupancy_type: str, number_stories: int
):
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
            table_name = "IRC 2006 W1 Design Level <=1500 SF"
        else:
            table_name = "IRC 2006 W1 Design Level >1500 SF"

    elif number_stories < 4:
        table_name = "IBC 2006 Low-Rise Design Level"

    elif number_stories > 4:
        table_name = "IBC 2006 Mid-Rise/High-Rise Design Level"

    return table_name

def process_honolulu_county(
    square_feet: float, year_built: int, occupancy_type: str, number_stories: int
):
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
                table_name = "IRC 2003 W1 Design Level <=1500 SF"
            else:
                table_name = "IRC 2006 W1 Design Level <=1500 SF"
        elif year_built <= 2012:
            table_name = "IRC 2003 W1 Design Level >1500 SF"
        else:
            table_name = "IRC 2006 W1 Design Level >1500 SF"

    elif number_stories < 4:
        if year_built <= 2012:
            table_name = "IBC 2003 Low-Rise Design Level"
        else:
            table_name = "IBC 2006 Low-Rise Design Level"

    elif number_stories > 4:
        if year_built <= 2012:
            table_name = "IBC 2003 Mid-Rise/High-Rise Design Level"
        else:
            table_name = "IBC 2006 Mid-Rise/High-Rise Design Level"

    return table_name

def process_maui_county(
    square_feet: float, year_built: int, occupancy_type: str, number_stories: int
):
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
            table_name = "IRC 2006 W1 Design Level <=1500 SF"
        else:
            table_name = "IRC 2006 W1 Design Level >1500 SF"

    elif number_stories < 4:
        table_name = "IBC 2006 Low-Rise Design Level"

    elif number_stories > 4:
        table_name = "IBC 2006 Mid-Rise/High-Rise Design Level"

    return table_name

def process_kauai_county(
    square_feet: float, year_built: int, occupancy_type: str, number_stories: int
):
    """
    Process points for Kauai County

    Args:
        square_feet (float) - building square footage
        year_built (int) - year the building was constructed
        occupancy_type (str) - occupancy type of the building
        number_of_stories (int) - number of floors

    Returns:
        table name to use
    """
    table_name = None

    if year_built < 2009:
        table_name = "pre-IBC"

    elif occupancy_type in ("RES1", "RES3A"):
        if square_feet <= 1500:
            if year_built <= 2012:
                table_name = "IRC 2003 W1 Design Level <=1500 SF"
            else:
                table_name = "IRC 2006 W1 Design Level <=1500 SF"
        elif year_built <= 2012:
            table_name = "IRC 2003 W1 Design Level >1500 SF"
        else:
            table_name = "IRC 2006 W1 Design Level >1500 SF"

    elif number_stories < 4:
        if year_built <= 2012:
            table_name = "IBC 2003 Low-Rise Design Level"
        else:
            table_name = "IBC 2006 Low-Rise Design Level"

    elif number_stories > 4:
        if year_built <= 2012:
            table_name = "IBC 2003 Mid-Rise/High-Rise Design Level"
        else:
            table_name = "IBC 2006 Mid-Rise/High-Rise Design Level"

    return table_name

def get_lookup_table_name(
    county_name: str, square_feet: float, year_built: int, occupancy_type: str, number_stories: int
):
    """
    Get the lookup table name for the building point.

    Args:
        county_name (str) - name of the county
        square_feet (float) - building square footage
        year_built (int) - year the building was constructed
        occupancy_type (str) - occupancy type of the building
        number_of_stories (int) - number of floors

    Returns:
        table name to use
    """
    table_name = None

    # TODO: Add logic for COM6, GOV2, EDU1 and EDU2
    if occupancy_type in ("COM6", "GOV2", "EDU1", "EDU2"):
        print(
            f"********Occupancy Type {occupancy_type} found.  NEED TO UPDATE!***********"
        )

    if county_name == "Hawaii":
        table_name = process_hawaii_county(
            square_feet, year_built, occupancy_type, number_stories
        )

    elif county_name == "Honolulu":
        table_name = process_honolulu_county(
            square_feet, year_built, occupancy_type, number_stories
        )

    elif county_name in ("Maui", "Kalawao"):
        table_name = process_maui_county(
            square_feet, year_built, occupancy_type, number_stories
        )

    elif county_name == "Kauai":
        table_name = process_maui_county(
            square_feet, year_built, occupancy_type, number_stories
        )

    return table_name

def get_pre_ibc_value(ubc_97_zone: str, year_built: int, occupancy_type: str):
    """
    Get the pre-IBC value from the pre-IBC table for Hawaii

    DesignLevelID       Design Level        Description 
    ---------------------------------------------------
        1                   PC              Pre Code 
        2                   LC              Low Code 
        3                   MC              Moderate Code 
        4                   HC              High Code 
        5                   LS              Low Code - Special 
        6                   MS              Moderate Code - Special  
        7                   HS              High Code - Special 

    Args:
        ubc_97_zone (int) - the UBC 97 Zone
        year_built (int) - year the building was constructed
        occupancy_type (str) - occupancy type of the building

    Returns:
        (int) The code level
    """
    design_level_id = -9999

    # UBC97Zone 4
    if ubc_97_zone == '4':
        if year_built <= 1963:
            design_level_id = 1
        elif year_built <= 1979:
            design_level_id = 3
        elif year_built > 1979 and occupancy_type in ("COM6", "GOV2", "EDU1", "EDU2"):
            design_level_id = 4            
        elif year_built > 1979 and occupancy_type in ("RES1", "RES3A"):
            design_level_id = 3

    # UBC97Zone 3
    elif ubc_97_zone == '3':
        if year_built <= 1963:
            design_level_id = 1
        elif year_built <= 1979:
            design_level_id = 2
        elif year_built > 1979 and occupancy_type in ("COM6", "GOV2", "EDU1", "EDU2"):
            design_level_id = 3        
        elif year_built > 1979 and occupancy_type in ("RES1", "RES3A"):
            design_level_id = 2

    # UBC97Zone 2
    elif ubc_97_zone == '2':
        if year_built <= 1963:
            design_level_id = 1
        elif year_built <= 1979:
            design_level_id = 2
        elif year_built > 1979 and occupancy_type in ("RES1", "RES3A"):
            design_level_id = 3

    # UBC97Zone 1
    elif ubc_97_zone == '1':
        if year_built <= 1979:
            design_level_id = 1
        elif year_built > 1979:
            design_level_id = 2

    return design_level_id         

def main(in_fc, i_code_table):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class to process.
        i_code_table - Table that contains the seismic design level codes.

    Returns:
        None
    """
    desc = arcpy.Describe(in_fc)
    oid_field = desc.oidFieldName

    fields = [
        "OID@",
        "Tract",
        "CountyName",
        "AreaSqft",
        "YEAR_BUILT",
        "Occupancy_Type",
        "NUM_STORIES",
        "UBC97Zone"
    ]
    with arcpy.da.SearchCursor(in_table=in_fc, field_names=fields) as cursor:
        for row in cursor:
            census_tract = row[1]
            county_name = row[2]
            square_feet = row[3]
            year_built = row[4]
            occupancy_type = row[5]
            number_stories = row[6]
            ubc_97_zone = row[7]

            design_level_id = -9999

            # Determine the table to use
            lookup_table_name = get_lookup_table_name(
                county_name=county_name, 
                square_feet=square_feet, 
                year_built=year_built, 
                occupancy_type=occupancy_type, 
                number_stories=number_stories)

            # Use the pre-IBC table
            if lookup_table_name == "pre-IBC":
                design_level_id = get_pre_ibc_value(ubc_97_zone=ubc_97_zone, 
                                                    year_built=year_built, 
                                                    occupancy_type=occupancy_type)

            # Use the CT_Icode table (derived from "BCS Design Levels for I-Codes for post-2000 Construction for 6 Seismic States.xlsx")
            if lookup_table_name in SEISMIC_CODES.keys():
                column_name = SEISMIC_CODES[lookup_table_name]
                where_clause = f"TRACT = '{census_tract}'"
                with arcpy.da.SearchCursor(i_code_table, [column_name], where_clause=where_clause) as table_cursor:
                    for table_row in table_cursor:
                        design_level_id = table_row[0]

            # Select the current row
            selected_row = arcpy.management.SelectLayerByAttribute(
                in_layer_or_view=in_fc, 
                selection_type="NEW_SELECTION", 
                where_clause=f"{oid_field} = {row[0]}")

            # Calculate the field
            arcpy.management.CalculateField(in_table=selected_row, 
                                            field="EqDesignLe", 
                                            expression=f"{design_level_id}", 
                                            expression_type="PYTHON3")


if __name__ == "__main__":
    script_dir = Path(__file__).parent
    data_folder = os.path.join(script_dir.parent, "data")
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "hi_uni.gdb\\hi_uni_points")
    hawii_icode_table = os.path.join(data_folder, "hi_uni_Seismic.gdb\\CT_ICode")

    main(in_fc=feature_class, i_code_table=hawii_icode_table)
