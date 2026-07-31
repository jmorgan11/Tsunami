"""
Filename: extract_census_tract.py
Purpose: Extract the Census Tract data for each point from the Census Data.
Author: Jesse Morgan
Date: 5/27/2026
Updates: None
"""
import os
import sys
from pathlib import Path
import arcpy


def main(in_fc, census_tract_data):
    """
    Extract the Census Tract for each point from the Census Data.

    Arguments:
        in_fc - Path the feature class to update.
        census_tract_data - The Census Tract data.

    Returns:
        None
    """
    try:
        # Determine the database the feature class is in
        desc = arcpy.Describe(value=in_fc)
        db_path = desc.path
        base_name = desc.name

        # Output path for the spatial join
        spatial_join_path = os.path.join(db_path, "census_tract_join")
        if arcpy.Exists(spatial_join_path):
            arcpy.management.Delete(os.path.join(db_path, "census_tract_join"))

        # Perform spatial join
        spatial_join = arcpy.analysis.SpatialJoin(
            target_features=in_fc,
            join_features=census_tract_data,
            out_feature_class=spatial_join_path,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            match_option="CLOSEST")

        # Drop extra fields
        for field_name in ["Join_Count", "TARGET_FID"]:
            arcpy.management.DeleteField(in_table=spatial_join, drop_field=field_name)

        # Delete the previous points feature class
        arcpy.management.Delete(in_data=in_fc)

        # Rename the spatial join feature class
        arcpy.management.Rename(in_data=spatial_join, out_data=os.path.join(db_path, base_name))

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    data_folder = os.path.join(script_dir.parent, "data")
    out_folder = os.path.join(script_dir.parent, "outputs")

    census_tracts = os.path.join(data_folder, "Census_Data.gdb\\Census_Tract_Population")
    feature_class = os.path.join(out_folder, "or_ucmb.gdb\\or_ucmb_points")

    main(in_fc=feature_class, census_tract_data=census_tracts)
