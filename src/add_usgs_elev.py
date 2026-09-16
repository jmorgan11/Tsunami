"""
Filename: add_usgs_elev.py
Purpose: Create a CSV from all the building points with the USGS NED 1/3 
         elevation values in feet added.
Author: Jesse Morgan
Date: 9/16/2026
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


def main(in_fc, dem, output_folder, process_fields):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class
        dem - The DEM to derived the elevation values from.
        output_folder - Path to export the CSV
        process_fields - Tuple of fields for processing (ID field, Longitude, Latitude)

    Returns:
        None
    """
    try:
        # Drop fields if it already exists
        if 'ned_1_3_elev_m' in [field.name for field in arcpy.ListFields(dataset=in_fc)]:
            arcpy.DeleteField_management(in_table=in_fc, drop_field='ned_1_3_elev_m')

        if 'USGS_ground_elev_ft' in [field.name for field in arcpy.ListFields(dataset=in_fc)]:
            arcpy.DeleteField_management(in_table=in_fc, drop_field='USGS_ground_elev_ft')

        # Extract the elevation value from the NED for each point
        ExtractMultiValuesToPoints(in_point_features=in_fc, in_rasters=dem)

        # Create the field to store elevation units in feet
        # NED elevations are in meters, so convert them to feet
        arcpy.management.CalculateField(
            in_table=in_fc,
            field="USGS_ground_elev_ft",
            expression=f"!ned_1_3_elev_m! * {METERS_TO_FEET}",
            expression_type="PYTHON3")

        # Delete the output file if it already exists
        out_name = os.path.basename(in_fc).replace("_points", "_usgs_elevation") + ".csv"

        if arcpy.Exists(os.path.join(output_folder, out_name)):
            arcpy.management.Delete(os.path.join(output_folder, out_name))

        # Export the feature class to a CSV
        arcpy.conversion.TableToTable(
            in_rows=in_fc,
            out_path=output_folder,
            out_name=out_name,
            field_mapping=f"Building ID \"{process_fields[0]}\" true true false 100 Text 0 0,First,#,{in_fc},{process_fields[0]},0,99;"
                          f"Longitude \"{process_fields[1]}\" true true false 8 Double 0 0,First,#,{in_fc},{process_fields[1]},-1,-1;"
                          f"Latitude \"{process_fields[2]}\" true true false 8 Double 0 0,First,#,{in_fc},{process_fields[2]},-1,-1;"
                          f"USGS_ground_elev_ft \"USGS_ground_elev_ft\" true true false 8 Double 0 0,First,#,{in_fc},USGS_ground_elev_ft,-1,-1")


    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    csv_output_folder = os.path.join(out_folder, "USGS_Elevation_CSVs")
    data_folder = os.path.join(script_dir.parent, "data")
    in_dem = os.path.join(data_folder, "NED_1_3.gdb\\ned_1_3_elev_m")
    fc_path = os.path.join(out_folder, "hi_tsu_unc_mb.gdb", "hi_tsu_unc_mb_full_points")
    req_fields = ("accntnum", "LON", "LAT")

    main(in_fc=fc_path, dem=in_dem, output_folder=csv_output_folder, process_fields=req_fields)
