"""
Filename: populate_fields.py
Purpose: Populate the necessary fields for the Hazus required inputs.
Author: Jesse Morgan
Date: 5/27/2026
Updates: None
"""
import os
import sys
from pathlib import Path
import arcpy


def main(folder_path, gdb_name):
    """
    Main function.

    Arguments:
        folder_path - the path to a folder where the GDB will be created.
        gdb_name - the name of the GDB to be created.

    Returns:
        The full path to the file geodatabase
    """
    # Convert the gdb_name to an acceptable format.
    file_gdb_name = arcpy.ValidateTableName(name=gdb_name).lower().replace(" ", "_")

    # Full path to the new file geodatabase
    file_geodatabase_path = os.path.join(folder_path, file_gdb_name) + ".gdb"

    # Check if the path exists
    if not os.path.exists(folder_path):
        print(f"\n{folder_path} does not exists. Exiting...")
        sys.exit(1)

    # Create the file geodatabase
    try:
        arcpy.management.CreateFileGDB(out_folder_path=folder_path, out_name=file_gdb_name)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        print(f"ERROR: {file_geodatabase_path} already exists.  Exiting...")
        sys.exit(1)

    return file_geodatabase_path

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    out_name = "MDI_OR_mb_20190228".lower()

    main(folder_path=out_folder, gdb_name=out_name)
