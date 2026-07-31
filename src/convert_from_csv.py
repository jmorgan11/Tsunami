"""
Filename: convert_from_csv.py
Purpose: Convert a CSV to a feature class in a file geodatabase.
Author: Jesse Morgan
Date: 5/27/2026
Updates: None
"""
import os
import sys
from pathlib import Path
import arcpy


def main(file_gdb_path, csv_path):
    """
    Main function.

    Arguments:
        file_gdb_path - Path the file geodatabase where the feature class will be created.
        csv_path - Path the CSV file to convert.

    Returns:
        The name of the feature class created.
    """
    # Create the feature class name
    base_name = os.path.basename(csv_path).lower().replace(" ", "_")
    strip_csv = base_name.replace(".csv", "")
    fc_name = strip_csv + "_full_points"

    # Create the point feature class
    try:
        arcpy.management.XYTableToPoint(
            in_table=csv_path,
            out_feature_class=os.path.join(file_gdb_path, fc_name),
            x_field="LON",
            y_field="LAT")
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        print("\nCould not create the point feature class here: "
              f"{os.path.join(file_gdb_path, fc_name)}")
        sys.exit(1)

    return fc_name


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    data_folder = os.path.join(script_dir.parent, "data")
    out_folder = os.path.join(script_dir.parent, "outputs")

    file_gdb = os.path.join(out_folder, "mdi_or_mb_20190228.gdb")
    csv_file = os.path.join(data_folder, "MDI_OR_mb_20190228.csv")

    main(file_gdb_path=file_gdb, csv_path=csv_file)
