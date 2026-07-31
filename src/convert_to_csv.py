"""
Filename: convert_to_csv.py
Purpose: Convert the feature class to a CSV.
Author: Jesse Morgan
Date: 5/27/2026
Updates: None
"""

import os
import sys
from pathlib import Path
import arcpy

def main(in_fc, output_folder):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class to process.
        output_folder - Location of the where the CSV will be created.

    Returns:
        None
    """
    try:
        # Create CSV output name.
        out_csv = os.path.join(output_folder, os.path.basename(in_fc) + ".csv")

        arcpy.conversion.TableToTable(
            in_rows=in_fc,
            out_path=output_folder,
            out_name= os.path.basename(in_fc) + ".csv",
            field_mapping=f"ID \"ID\" true true false 100 Text 0 0,First,#,{in_fc},ID,0,99;"
                          f"EqBldgType \"EqBldgType\" true true false 4 Long 0 0,First,#,{in_fc},EqBldgType,-1,-1;"
                          f"EdgBldgTypeClass \"EdgBldgTypeClass\" true true false 4 Text 0 0,First,#,{in_fc},EdgBldgTypeClass,0,3;"
                          f"LMH_Rise \"LMH_Rise\" true true false 4 Text 0 0,First,#,{in_fc},LMH_Rise,0,3;"
                          f"EqDesignLe \"EqDesignLe\" true true false 4 Long 0 0,First,#,{in_fc},EqDesignLe,-1,-1;"
                          f"SOccupID \"SOccupID\" true true false 4 Text 0 0,First,#,{in_fc},SOccupID,0,3;"
                          f"Occupancy_Type \"Occupancy_Type\" true true false 5 Text 0 0,First,#,{in_fc},Occupancy_Type,0,4;"
                          f"FirstFloor \"FirstFloor\" true true false 4 Long 0 0,First,#,{in_fc},FirstFloor,-1,-1;"
                          f"ValStruct \"ValStruct\" true true false 4 Long 0 0,First,#,{in_fc},ValStruct,-1,-1;"
                          f"ValCont \"ValCont\" true true false 4 Long 0 0,First,#,{in_fc},ValCont,-1,-1;"
                          f"AreaSqft \"AreaSqft\" true true false 8 Double 0 0,First,#,{in_fc},AreaSqft,-1,-1;"
                          f"CBFips \"CBFips\" true true false 15 Text 0 0,First,#,{in_fc},CBFips,0,14;"
                          f"SiteElevation_UserDefined_ft \"SiteElevation_UserDefined_ft\" true true false 8 Double 0 0,First,#,{in_fc},SiteElevation_UserDefined_ft,-1,-1;"
                          f"BldgHeight_ft \"BldgHeight_ft\" true true false 8 Double 0 0,First,#,{in_fc},BldgHeight_ft,-1,-1;"
                          f"BuildingLimit \"BuildingLimit\" true true false 8 Double 0 0,First,#,{in_fc},BuildingLimit,-1,-1;"
                          f"ContentLimit \"ContentLimit\" true true false 512 Text 0 0,First,#,{in_fc},ContentLimit,0,511;"
                          f"BuildingDeductible \"BuildingDeductible\" true true false 8 Double 0 0,First,#,{in_fc},BuildingDeductible,-1,-1;"
                          f"ContentDeductible \"ContentDeductible\" true true false 8 Double 0 0,First,#,{in_fc},ContentDeductible,-1,-1;"
                          f"geometry \"geometry\" true true false 512 Text 0 0,First,#,{in_fc},geometry,0,511;"
                          f"Longitude \"Longitude\" true true false 8 Double 0 0,First,#,{in_fc},Longitude,-1,-1;"
                          f"Latitude \"Latitude\" true true false 8 Double 0 0,First,#,{in_fc},Latitude,-1,-1")


    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "or_ucmb.gdb/or_ucmb_points")

    main(in_fc=feature_class, output_folder=out_folder)

