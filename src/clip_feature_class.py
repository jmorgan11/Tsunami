"""
Filename: clip_feature_class.py
Purpose: Clip the full feature class to the Tsunami polygon extents.
Author: Jesse Morgan
Date: 5/27/2026
Updates: None
"""
import os
import sys
from pathlib import Path
import arcpy

def main(in_fc, tsunami_polygon):
    """
    Main function.

    Arguments:
        in_fc - Path the feature class to be clipped.
        tsunami_polygon - Path the Tsunami polygons to clip to.

    Returns:
        out_fc_name (str) - The name of the clipped feature class created.
    """
    out_fc_name = os.path.basename(in_fc).replace("_full_points", "") + "_points"
    geodatabase_path = os.path.dirname(in_fc)

    try:
        arcpy.analysis.Clip(
            in_features=in_fc,
            clip_features=tsunami_polygon,
            out_feature_class=os.path.join(geodatabase_path, out_fc_name))
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        print("\nERROR: Could not clip the feature class.")
        sys.exit(1)

    return out_fc_name

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    data_folder = os.path.join(script_dir.parent, "data")
    out_folder = os.path.join(script_dir.parent, "outputs")

    feature_class = os.path.join(out_folder, "or_ucmb.gdb/or_ucmb_points")

    tsunami_fc = os.path.join(
        data_folder,
        "ASCE_Tsunami_Design_Zones.gdb/ts2022_Tsunami_Design_Zone")

    main(in_fc=feature_class, tsunami_polygon=tsunami_fc)
