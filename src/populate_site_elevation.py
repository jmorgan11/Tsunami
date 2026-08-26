"""
Filename: populate_site_elevation.py
Purpose: Populate the SiteElevation_UserDefined_ft field
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
from arcpy.sa import ExtractMultiValuesToPoints

METERS_TO_FEET = 3.2808399

def main(in_fc, dem):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class to process.
        dem - The DEM to derived the elevation values from.

    Returns:
        None
    """
    try:
        # Drop the field if it already exists
        if 'ned_1_3_tsunami_zones' in [field.name for field in arcpy.ListFields(dataset=in_fc)]:
            arcpy.DeleteField_management(in_table=in_fc, drop_field='ned_1_3_tsunami_zones')

        # Extract the elevation value from the NED for each point
        ExtractMultiValuesToPoints(in_point_features=in_fc, in_rasters=dem)

        # Calculate the SiteElevation_UserDefined_ft field
        arcpy.management.CalculateField(
            in_table=in_fc,
            field="SiteElevation_UserDefined_ft",
            expression=f"!ned_1_3_tsunami_zones! * {METERS_TO_FEET}",
            expression_type="PYTHON3")

        # Drop the field
        arcpy.DeleteField_management(in_table=in_fc, drop_field='ned_1_3_tsunami_zones')

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    data_folder = os.path.join(script_dir.parent, "data")
    in_dem = os.path.join(data_folder, "NED_1_3.gdb\\ned_1_3_tsunami_zones")
    feature_class = os.path.join(out_folder, "or_ucmb.gdb\\or_ucmb_points")

    main(in_fc=feature_class, dem=in_dem)
