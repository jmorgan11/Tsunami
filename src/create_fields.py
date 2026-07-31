"""
Filename: create_fields.py
Purpose: Create the necessary fields for the Hazus required inputs.
Author: Jesse Morgan
Date: 5/27/2026
Updates: None
"""
import sys
import os
from pathlib import Path
import arcpy


FIELDS_DICT = {
    "BuildingValue_Average": ["DOUBLE"],
    "Pop2pm": ["DOUBLE"],
    "Pop2am": ["DOUBLE"],
    "FoundTypeId": ["LONG"],
    "PerSqftAvgVal": ["DOUBLE"],
    "Pop2pmU65": ["DOUBLE"],
    "Pop2pmO65": ["DOUBLE"],
    "Pop2amU65": ["DOUBLE"],
    "Pop2amO65": ["DOUBLE"],
    "ID": ["TEXT", 100],
    "EqBldgType": ["LONG"],
    "EdgBldgTypeClass": ["TEXT", 4],
    "LMH_Rise": ["TEXT", 4],
    "EqDesignLe": ["LONG"],
    "SOccupID": ["LONG"],
    "Occupancy_Type": ["TEXT", 5],
    "FirstFloor": ["LONG"],
    "ValStruct": ["LONG"],
    "ValCont": ["LONG"],
    "AreaSqft": ["DOUBLE"],
    "SiteElevation_UserDefined_ft": ["DOUBLE"],
    "BldgHeight_ft": ["DOUBLE"],
    "DefaultBldgHeight_Flag": ["LONG"],
    "BuildingLimit": ["DOUBLE"],
    "DefaultBldgCap_Flag": ["LONG"],
    "BuildingDeductible": ["DOUBLE"],
    "DefaultBldgDeductible_Flag": ["LONG"],
    "ContentDeductible": ["DOUBLE"],
    "DefaultContDeductible_Flag": ["LONG"],
    "geometry": ["TEXT", 512],
    "Longitude": ["DOUBLE"],
    "Latitude": ["DOUBLE"],
}

def main(in_fc):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class to add the fields to.

    Returns:
        None
    """
    # Iterate through the dictionary, adding the fields
    try:
        for field, values in FIELDS_DICT.items():
            if values[0] == "TEXT":
                # Add the TEXT fields
                arcpy.management.AddField(
                    in_table=in_fc,
                    field_name=field,
                    field_type=values[0],
                    field_length=values[1])

                # Calculate the NsiID field to OBJECTID.  Otherwise, use "UNK"
                if field == "NsiID":
                    expression = "!OBJECTID!"
                else:
                    expression = "\"UNK\""

                arcpy.management.CalculateField(
                    in_table=in_fc,
                    field=field,
                    expression=expression,
                    expression_type="PYTHON3")
            else:
                # Add Numeric fields
                arcpy.management.AddField(
                    in_table=in_fc,
                    field_name=field,
                    field_type=values[0])

                # Calculate it to -9999
                arcpy.management.CalculateField(
                    in_table=in_fc,
                    field=field,
                    expression=-9999,
                    expression_type="PYTHON3")
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        print(f"ERROR: Could not add the field '{field}' and calculate it.  Exiting...")
        sys.exit(1)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "or_ucmb.gdb\\or_ucmb_points")

    main(in_fc=feature_class)
