"""
Filename: populate_found_type_id.py
Purpose: Populate the FoundTypeID field
Author: Jesse Morgan
Date: 5/29/2026
Updates: None

foundation type (Milliman)                  HAZUS
---------------------------------------------------------------------
2 = basement                                   4
4 = crawlspace                                 5
6 = pier                                       2
7 = fill or wall                               6
8 = slab                                       7
9 = pile                                       1

Note: Scope of work only includes California, Oregon, Washington, Alaska and Hawaii.

Note: Code is only written for MDI data.
"""
import os
import sys
from pathlib import Path
import arcpy

def calc_foundation_tye(in_fc):
    """
    Populate the FoundTypeID field

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminator based on the data source.
    found_type = arcpy.AddFieldDelimiters(in_fc, "FoundationType")

    for foundation_code in [2, 4, 6, 7, 8, 9]:

        # Create the SQL expression to select the rows.
        sql_exp = f"{found_type} = {foundation_code}"

        out_code = -9999
        if foundation_code == 2:
            out_code = 4
        elif foundation_code == 4:
            out_code = 5
        elif foundation_code == 6:
            out_code = 2
        elif foundation_code == 7:
            out_code = 6
        elif foundation_code == 8:
            out_code = 7
        elif foundation_code == 9:
            out_code = 1

        try:
            # Select the rows.
            selected_rows = arcpy.management.SelectLayerByAttribute(
                in_layer_or_view=in_fc,
                selection_type="NEW_SELECTION",
                where_clause=sql_exp)

            # Calculate the FoundTypeID for the selected rows.
            arcpy.management.CalculateField(
                in_table=selected_rows,
                field="FoundTypeID",
                expression=f"{out_code}",
                expression_type="PYTHON3")
        except arcpy.ExecuteError:
            print(arcpy.GetMessages())
            sys.exit(1)

def main(in_fc):
    """
    Main function.

    Arguments:
        in_fc - Path to the feature class to process.

    Returns:
        None
    """
    calc_foundation_tye(in_fc=in_fc)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "or_ucmb.gdb\\or_ucmb_points")

    main(in_fc=feature_class)