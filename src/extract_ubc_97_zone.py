"""
Filename: extract_ubc_97_zone.py
Purpose: Extract the UBC97Zone value for each point
Author: Jesse Morgan
Date: 9/17/2026
Updates: None
"""
import os
import sys
from pathlib import Path
import arcpy


def main(in_fc, ubc_97_fc):
    """
    Extract the UBC97Zone value for each point.

    Arguments:
        in_fc - Path the feature class to update.
        ubc_97_fc - The UBC97 feature class.

    Returns:
        None
    """
    try:
        # Determine the database the feature class is in
        desc = arcpy.Describe(value=in_fc)
        db_path = desc.path
        base_name = desc.name

        # Output path for the spatial join
        spatial_join_path = os.path.join(db_path, "ubc97_join")
        if arcpy.Exists(spatial_join_path):
            arcpy.management.Delete(os.path.join(db_path, "ubc97_join"))

        # Perform spatial join
        spatial_join = arcpy.analysis.SpatialJoin(
            target_features=in_fc,
            join_features=ubc_97_fc,
            out_feature_class=spatial_join_path,
            join_operation="JOIN_ONE_TO_ONE",
            join_type="KEEP_ALL",
            match_option="CLOSEST")

        # Drop extra fields
        for field_name in ["Join_Count", "TARGET_FID", 'Tract', 'CountyFips', 'Tract6', 'TractArea', 
                           'CenLongit', 'CenLat', 'Place', 'County', 'County_FIPS', 'State_FIPS', 
                           'St_Co_FIPS', 'Place_FIPS', 'Combined_Hazard_Code', 'Hurricane_Code', 
                           'Flood_Code', 'Seismic_Code', 'Tornado_Code', 'Wind_Code', 'Flood_Risk', 
                           'Seismic_Risk', 'Hurricane_Risk', 'Tornado_Risk', 'Wind_Risk', 
                           'Hazard_Risk', 'ST_Abbrev', 'Data_Currency', 'JoinID', 'Building_Code', 
                           'Res_Code', 'Weakened_Seismic', ]:
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
    ubc_97_fc = os.path.join(data_folder, "2023-06-28-ReferenceData.gdb\\Tracts_2020_BCAT_lookup_wUBC97")
    feature_class = os.path.join(out_folder, "hi_uni.gdb\\hi_uni_points")

    main(in_fc=feature_class, ubc_97_fc=ubc_97_fc)
