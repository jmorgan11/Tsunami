"""
Filename: populate_building_deduct.py
Purpose: Populate the BuildingDeductible and DefaultBldgDeductible_Flag fields
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

def main(in_fc):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class to process.

    Returns:
        None
    """
    try:
        # Calculate the BuildingDeductible
        arcpy.management.CalculateField(
            in_table=in_fc,
            field="BuildingDeductible",
            expression="!BLDG_DED!",
            expression_type="PYTHON3")

        # Calculate the DefaultBldgDeductible_Flag
        arcpy.management.CalculateField(
            in_table=in_fc,
            field="DefaultBldgDeductible_Flag",
            expression="0",
            expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "hi_tsu_unc_mb.gdb\\hi_tsu_unc_mb_points")

    main(in_fc=feature_class)