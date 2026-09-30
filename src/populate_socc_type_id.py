"""
Filename: populate_socc_type_id.py
Purpose: Populate the SOccupID field
Author: Jesse Morgan
Date: 5/29/2026
Updates: None

Note: Scope of work only includes California, Oregon, Washington, Alaska and Hawaii.

Building Type - Hazus 
-----------------------------------------------------------------------------
RES2  - MOBILE_MANUFACTURED_HOME
  ?   - NON_RESIDENTIAL_BUILDING
RES3A - ONE_TO_FOUR_FAMILY_BUILDING
RES1? - OTHER_RESIDENTIAL_BUILDING
RES3A - RESIDENTIAL_CONDOMINIUM_BUILDING and NUM_UNITS is  1 -  2
RES3B - RESIDENTIAL_CONDOMINIUM_BUILDING and NUM_UNITS is  3 -  4
RES3C - RESIDENTIAL_CONDOMINIUM_BUILDING and NUM_UNITS is  5 -  9
RES3D - RESIDENTIAL_CONDOMINIUM_BUILDING and NUM_UNITS is 10 - 19
RES3E - RESIDENTIAL_CONDOMINIUM_BUILDING and NUM_UNITS is 20 - 40
RES3F - RESIDENTIAL_CONDOMINIUM_BUILDING and NUM_UNITS is 50+
RES1  - RESIDENTIAL_UNIT

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
        # Calculate the SOccupID for the selected rows.
        arcpy.management.CalculateField(
            in_table=in_fc,
            field="SOccupID",
            expression='1',
            expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "or_ucmb.gdb\\or_ucmb_points")

    main(in_fc=feature_class)

# TODO: Update code for new SOccupID logic. The current logic is a placeholder and needs to be replaced with the 
#       actual logic for determining the SOccupID based on the MDI data.