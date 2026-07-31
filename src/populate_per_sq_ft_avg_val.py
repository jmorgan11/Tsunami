"""
Filename: populate_per_sq_ft_avg_val.py
Purpose: Populate the PerSqftAvgVal.  The AreaSqft field will also be populated as part
         of the intermediate logic.
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

def calc_no_basement(in_fc):
    """
    Calculate the PerSqftAvgVal for buildings with no basement

    Args:
        in_fc: The feature class to update

    Returns:
        None
    """
    try:
        # Create field deliminator based on the data source.
        basement_type = arcpy.AddFieldDelimiters(in_fc, "BasementFinishType")
        num_stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")

        for stories in [1, 2, 3]:

            # Create the SQL expression to select the rows.
            sql_exp = f"{basement_type} = 0 AND {num_stories} = {stories}"

            out_value = -9999
            if stories == 1:
                out_value = 128.20
            elif stories == 2:
                out_value = 132.88
            elif stories == 3:
                out_value = 137.43

            # Select the rows.
            selected_rows = arcpy.management.SelectLayerByAttribute(
                in_layer_or_view=in_fc,
                selection_type="NEW_SELECTION",
                where_clause=sql_exp)

            # Calculate the PerSqftAvgVal for the selected rows.
            arcpy.management.CalculateField(
                in_table=selected_rows,
                field="PerSqftAvgVal",
                expression=f"{out_value}",
                expression_type="PYTHON3")

            # Calculate the AreaSqft for the selected rows.
            arcpy.management.CalculateField(
                in_table=selected_rows,
                field="AreaSqft",
                expression="!BLDG_VALUE! / !PerSqftAvgVal!",
                expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def get_fips_list(in_fc):
    """
    Get a list of unique FIPs codes in the dataset
    Args:
        in_fc - The input feature class

    Returns:
        A list of unique FIPs codes
    """
    try:
        all_fips = []

        with arcpy.da.SearchCursor(in_table=in_fc, field_names=["CountyFips"]) as cursor:
            for row in cursor:
                if row[0]:
                    all_fips.append(row[0])

        return list(set(all_fips))

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_building_value_average_field(in_fc, in_fips_list):
    """
    Calculate the BuildingValue_Average field
    Args:
        in_fc - The input feature class
        in_fips_list - A list of FIPs codes to process

    Returns:
        None
    """
    try:
        # Create field deliminator based on the data source.
        basement_type = arcpy.AddFieldDelimiters(in_fc, "BasementFinishType")
        num_stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")
        cb_fips = arcpy.AddFieldDelimiters(in_fc, "CountyFips")

        for stories in [1, 2, 3]:
            for fips in in_fips_list:
                building_values = 0
                num_of_records = 0
                avg_building_value = 0

                # Create the SQL expression to select the rows.
                sql_exp = f"{basement_type} <> 0 AND {num_stories} = {stories} AND {cb_fips} = '{fips}'"

                with arcpy.da.SearchCursor(in_table=in_fc, field_names=["BLDG_VALUE"], where_clause=sql_exp) as cursor:
                    for row in cursor:
                        building_values += row[0]
                        num_of_records += 1

                if num_of_records > 0:
                        avg_building_value = building_values / num_of_records

                # Select the rows.
                selected_rows = arcpy.management.SelectLayerByAttribute(
                    in_layer_or_view=in_fc,
                    selection_type="NEW_SELECTION",
                    where_clause=sql_exp)

                # Calculate the BuildingValue_Average for the selected rows.
                arcpy.management.CalculateField(
                    in_table=selected_rows,
                    field="BuildingValue_Average",
                    expression=f"{avg_building_value}",
                    expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_with_basement(in_fc):
    """
    Calculate the PerSqftAvgVal for buildings with a basement

    Args:
        in_fc - The feature class to update

    Returns:
        None
    """
    try:
        # Create field deliminator based on the data source.
        basement = arcpy.AddFieldDelimiters(in_fc, "BasementFinishType")

        # Create the SQL expression to select the rows.
        sql_exp = f"{basement} > 0"

        process_fields = ["BLDG_VALUE", "NUM_STORIES", "BuildingValue_Average",
                          "AreaSqft", "PerSqftAvgVal"]

        with arcpy.da.UpdateCursor(in_table=in_fc, field_names=process_fields, where_clause=sql_exp) as cursor:
            for row in cursor:
                bldg_value = row[0]
                num_stories = row[1]
                bldg_val_avg = row[2]

                if bldg_value > bldg_val_avg:
                    if num_stories == 1:
                        row[3] = bldg_value / 168.75
                        row[4] = 168.75
                    elif num_stories == 2:
                        row[3] = bldg_value / 158.08
                        row[4] = 158.08
                    elif num_stories == 3:
                        row[3] = bldg_value / 158.88
                        row[4] = 156.88

                if bldg_value <= bldg_val_avg:
                    if num_stories == 1:
                        row[3] = bldg_value / 140.95
                        row[4] = 140.95
                    elif num_stories == 2:
                        row[3] = bldg_value / 140.98
                        row[4] = 140.98
                    elif num_stories == 3:
                        row[3] = bldg_value / 143.73
                        row[4] = 143.73

                # Update the cursor with the updated list
                cursor.updateRow(row)

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
    print("\tCalculating no Basement...")
    calc_no_basement(in_fc=in_fc)

    print("\tGetting unique FIPs codes...")
    fips_codes = get_fips_list(in_fc=in_fc)

    print("\tCalculating Building Value Average field...")
    calc_building_value_average_field(in_fc=in_fc, in_fips_list=fips_codes)

    print("\tCalculating with Basement...")
    calc_with_basement(in_fc=in_fc)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "hi_ucmb.gdb\\hi_ucmb_points")

    main(in_fc=feature_class)
