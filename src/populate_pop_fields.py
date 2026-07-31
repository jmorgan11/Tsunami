"""
Filename: populate_pop_fields.py
Purpose: Populate the Pop2pmU65, Pop2pmO65, Pop2amU65 and Pop2amO65 fields
Author: Jesse Morgan
Date: 5/29/2026
Updates: None

Note: Scope of work only includes California, Oregon, Washington, Alaska and Hawaii.

Note: Code is only written for MDI data.
"""
import os
import sys
from pathlib import Path
import arcpy

def calc_2pm_2am_fields(in_fc):
    """
    Populate the intermediate Pop2pm and P2am fields

    Note: The values of 1201 and 841 are from table 5-32 in the Hazus 6.1 Inventory
    Technical Manual for RES1 Occupancy codes

    Args:
        in_fc - The feature class to update

    Returns:
        None
    """
    try:
        arcpy.management.CalculateField(in_table=in_fc,
                                        field="Pop2pm",
                                        expression_type="PYTHON3",
                                        expression="!AreaSqft! / 1201")

        arcpy.management.CalculateField(in_table=in_fc,
                                        field="Pop2am",
                                        expression_type="PYTHON3",
                                        expression="!AreaSqft! / 841")


    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)


def calc_pop_fields(in_fc):
    """
    Calculate the Pop2pmU65, Pop2pmO65, Pop2amU65 and Pop2amO65 fields

    Args:
        in_fc - The feature class to update

    Returns:
        None
    """
    try:
        arcpy.management.CalculateField(in_table=in_fc,
                                        field="Pop2pmU65",
                                        expression_type="PYTHON3",
                                        expression="!PopUnder65_Pct! * !Pop2pm!")

        arcpy.management.CalculateField(in_table=in_fc,
                                        field="Pop2pmO65",
                                        expression_type="PYTHON3",
                                        expression="!PopOver65_Pct! * !Pop2pm!")

        arcpy.management.CalculateField(in_table=in_fc,
                                        field="Pop2amU65",
                                        expression_type="PYTHON3",
                                        expression="!PopUnder65_Pct! * !Pop2am!")

        arcpy.management.CalculateField(in_table=in_fc,
                                        field="Pop2amO65",
                                        expression_type="PYTHON3",
                                        expression="!PopOver65_Pct! * !Pop2am!")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)


def main(in_fc):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class to process.

    Returns:
        None
    """
    calc_2pm_2am_fields(in_fc=in_fc)
    calc_pop_fields(in_fc=in_fc)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "or_ucmb.gdb\\or_ucmb_points")

    main(in_fc=feature_class)