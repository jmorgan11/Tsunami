"""
Filename: populate_lmh_rise_and_bldg_ht.py
Purpose: Populate the LHM_Rise, BldgHeight_ft and DefaultBldgHeight_Flag
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

def calc_low(in_fc):
    """
    Populate the LMH_Rise of Low for stories less than 4

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")

    # Create the SQL expression to select the rows.
    sql_exp = f"{stories} < 4"

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the LMH_Rise for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="LMH_Rise",
            expression="'Low'",
            expression_type="PYTHON3")

        # Calculate the BldgHeight_ft for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="BldgHeight_ft",
            expression="!NUM_STORIES! * 11",
            expression_type="PYTHON3")

        # Calculate the DefaultBldgHeight_Flag for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="DefaultBldgHeight_Flag",
            expression="1",
            expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_mid(in_fc):
    """
    Populate the LMH_Rise of Mid for stories between 4 and 7 inclusive

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")

    # Create the SQL expression to select the rows.
    sql_exp = f"{stories} >= 4 AND {stories} <= 7"

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the LMH_Rise for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="LMH_Rise",
            expression="'Mid'",
            expression_type="PYTHON3")

        # Calculate the BldgHeight_ft for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="BldgHeight_ft",
            expression="!NUM_STORIES! * 11",
            expression_type="PYTHON3")

        # Calculate the DefaultBldgHeight_Flag for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="DefaultBldgHeight_Flag",
            expression="1",
            expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_high(in_fc):
    """
    Populate the LMH_Rise of High for stories greater than 7

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")

    # Create the SQL expression to select the rows.
    sql_exp = f"{stories} > 7"

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the LMH_Rise for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="LMH_Rise",
            expression="'High'",
            expression_type="PYTHON3")

        # Calculate the BldgHeight_ft for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="BldgHeight_ft",
            expression="!NUM_STORIES! * 11",
            expression_type="PYTHON3")

        # Calculate the DefaultBldgHeight_Flag for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="DefaultBldgHeight_Flag",
            expression="1",
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
    calc_low(in_fc=in_fc)
    calc_mid(in_fc=in_fc)
    calc_high(in_fc=in_fc)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "or_ucmb.gdb\\or_ucmb_points")

    main(in_fc=feature_class)


# TODO: If different building types are available in the updated Uncorrelated dataset, 
#       the BldgHeight_ft calculation may need to be updated to reflect the different building types.  
#       NUM_STORY relationship:  
#          Residential (RES*, excluding RES4): 11 ft/story 
#          Hotel (RES4): 11.5 ft/story 
#          Office (COM*): 13.5 ft/story 
#          Other (IND, REL, GOV, EDU): 11.5 ft/story 
#          Buildings with >20 stories: +20 ft (mechanical/roof allowance) 