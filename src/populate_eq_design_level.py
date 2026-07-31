"""
Filename: populate_eq_design_level.py
Purpose: Populate Earthquake Design Level (EqDesignLe) field.
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


def calc_pc(in_fc, in_state_abbrev):
    """
    Populate the Earthquake Design Level of PC (Pre-Code)

    Arguments:
        in_fc - The feature class to update.
        in_state_abbrev - The state abbreviation.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    state_abbrev = arcpy.AddFieldDelimiters(in_fc, "StateAbbr")
    year_built = arcpy.AddFieldDelimiters(in_fc, "YEAR_BUILT")

    # Create the SQL expression to select the rows.
    sql_exp = None
    if in_state_abbrev == "AK": # Alaska
        sql_exp = f"{state_abbrev} = 'AK' AND " \
                  f"{year_built} <= 1964"

    elif in_state_abbrev == "CA": # California
        sql_exp = f"{state_abbrev} = 'CA' AND " \
                  f"{year_built} <= 1940"

    elif in_state_abbrev == "HI": # Hawaii
        sql_exp = f"{state_abbrev} = 'HI' AND " \
                  f"{year_built} <= 1974"

    elif in_state_abbrev == "OR": # Oregon
        sql_exp = f"{state_abbrev} = 'OR' AND " \
                  f"{year_built} <= 1974"

    elif in_state_abbrev == "WA": # Washington
        sql_exp = f"{state_abbrev} = 'WA' AND " \
                  f"{year_built} <= 1955"

    # Check if the SQL expression is empty.
    if not sql_exp:
        print("\tWARNING: No query created. No update performed.")
        return

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqDesignLe for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqDesignLe",
            expression="1",
            expression_type="PYTHON3")
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_lc(in_fc, in_state_abbrev):
    """
    Populate the Earthquake Design Level of LC (Low Code)

    Arguments:
        in_fc - The feature class to update.
        in_state_abbrev - The state abbreviation.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    state_abbrev = arcpy.AddFieldDelimiters(in_fc, "StateAbbr")
    year_built = arcpy.AddFieldDelimiters(in_fc, "YEAR_BUILT")

    # Create the SQL expression to select the rows.
    sql_exp = None
    if in_state_abbrev == "AK": # Alaska
        sql_exp = f"{state_abbrev} = 'AK' AND " \
                  f"{year_built} >= 1965 AND " \
                  f"{year_built} <= 1994"

    elif in_state_abbrev == "CA": # California
        sql_exp = f"{state_abbrev} = 'CA' AND " \
                  f"{year_built} >= 1941 AND " \
                  f"{year_built} <= 1975"

    elif in_state_abbrev == "HI": # Hawaii
        sql_exp = f"{state_abbrev} = 'HI' AND " \
                  f"{year_built} >= 1975 AND " \
                  f"{year_built} <= 1994"

    elif in_state_abbrev == "OR": # Oregon
        sql_exp = f"{state_abbrev} = 'OR' AND " \
                  f"{year_built} >= 1975 AND " \
                  f"{year_built} <= 1994"

    elif in_state_abbrev == "WA": # Washington
        sql_exp = f"{state_abbrev} = 'WA' AND " \
                  f"{year_built} >= 1956 AND " \
                  f"{year_built} <= 1974"

    # Check if the SQL expression is empty.
    if not sql_exp:
        print("\tWARNING: No query created. No update performed.")
        return

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqDesignLe for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqDesignLe",
            expression="2",
            expression_type="PYTHON3")
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_mc(in_fc, in_state_abbrev):
    """
    Populate the Earthquake Design Level of MC (Moderate Code)

    Arguments:
        in_fc - The feature class to update.
        in_state_abbrev - The state abbreviation.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    state_abbrev = arcpy.AddFieldDelimiters(in_fc, "StateAbbr")
    year_built = arcpy.AddFieldDelimiters(in_fc, "YEAR_BUILT")

    # Create the SQL expression to select the rows.
    sql_exp = None
    if in_state_abbrev == "AK": # Alaska
        sql_exp = f"{state_abbrev} = 'AK' AND " \
                  f"{year_built} >= 1995 AND " \
                  f"{year_built} <= 2000"

    elif in_state_abbrev == "CA": # California
        sql_exp = f"{state_abbrev} = 'CA' AND " \
                  f"{year_built} >= 1976 AND " \
                  f"{year_built} <= 1994"

    elif in_state_abbrev == "HI": # Hawaii
        sql_exp = f"{state_abbrev} = 'HI' AND " \
                  f"{year_built} >= 1995 AND " \
                  f"{year_built} <= 2000"

    elif in_state_abbrev == "OR": # Oregon
        sql_exp = f"{state_abbrev} = 'OR' AND " \
                  f"{year_built} >= 1995 AND " \
                  f"{year_built} <= 2000"

    elif in_state_abbrev == "WA": # Washington
        sql_exp = f"{state_abbrev} = 'WA' AND " \
                  f"{year_built} >= 1975 AND " \
                  f"{year_built} <= 2003"

    # Check if the SQL expression is empty.
    if not sql_exp:
        print("\tWARNING: No query created. No update performed.")
        return

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqDesignLe for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqDesignLe",
            expression="3",
            expression_type="PYTHON3")
        
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_hc(in_fc, in_state_abbrev):
    """
    Populate the Earthquake Design Level of HC (High Code)

    Arguments:
        in_fc - The feature class to update.
        in_state_abbrev - The state abbreviation.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    state_abbrev = arcpy.AddFieldDelimiters(in_fc, "StateAbbr")
    year_built = arcpy.AddFieldDelimiters(in_fc, "YEAR_BUILT")

    # Create the SQL expression to select the rows.
    sql_exp = None
    if in_state_abbrev == "AK": # Alaska
        sql_exp = f"{state_abbrev} = 'AK' AND " \
                  f"{year_built} >= 2001"

    elif in_state_abbrev == "CA": # California
        sql_exp = f"{state_abbrev} = 'CA' AND " \
                  f"{year_built} >= 1995 AND " \
                  f"{year_built} <= 2000"

    elif in_state_abbrev == "HI": # Hawaii
        sql_exp = f"{state_abbrev} = 'HI' AND " \
                  f"{year_built} >= 2001"

    elif in_state_abbrev == "OR": # Oregon
        sql_exp = f"{state_abbrev} = 'OR' AND " \
                  f"{year_built} >= 2001"

    elif in_state_abbrev == "WA": # Washington
        sql_exp = f"{state_abbrev} = 'WA' AND " \
                  f"{year_built} >= 2004"

    # Check if the SQL expression is empty.
    if not sql_exp:
        print("\tWARNING: No query created. No update performed.")
        return

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqDesignLe for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqDesignLe",
            expression="4",
            expression_type="PYTHON3")
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_hs(in_fc, in_state_abbrev):
    """
    Populate the Earthquake Design Level of HS (High Code - Special)

    Arguments:
        in_fc - The feature class to update.
        in_state_abbrev - The state abbreviation.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    state_abbrev = arcpy.AddFieldDelimiters(in_fc, "StateAbbr")
    year_built = arcpy.AddFieldDelimiters(in_fc, "YEAR_BUILT")

    # Create the SQL expression to select the rows.
    sql_exp = None
    if in_state_abbrev == "CA": # California
        sql_exp = f"{state_abbrev} = 'CA' AND " \
                  f"{year_built} >= 2001"

    # Check if the SQL expression is empty.
    if not sql_exp:
        print("\tWARNING: No query created. No update performed.")
        return

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqDesignLe for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqDesignLe",
            expression="7",
            expression_type="PYTHON3")
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_uniform_mc(in_fc):
    """
    Populate the Earthquake Design Level of MC (Moderate Code) for all rows.

    Arguments:
        in_fc - The feature class to update.
    """
    try:
        # Calculate the EqDesignLe for the selected rows.
        arcpy.management.CalculateField(
            in_table=in_fc,
            field="EqDesignLe",
            expression="3",
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
    for state_abbrev in ["AK", "CA", "HI", "OR", "WA"]:
        # For the uniform Millliman data, we will set all to MC (Moderate Code)
        if "uni" in in_fc.lower():
            calc_uniform_mc(in_fc=in_fc)
        else:
            calc_pc(in_fc=in_fc, in_state_abbrev=state_abbrev)
            calc_lc(in_fc=in_fc, in_state_abbrev=state_abbrev)
            calc_mc(in_fc=in_fc, in_state_abbrev=state_abbrev)
            calc_hc(in_fc=in_fc, in_state_abbrev=state_abbrev)
            if state_abbrev == "CA":
                calc_hs(in_fc=in_fc, in_state_abbrev=state_abbrev)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "or_uni.gdb\\or_uni_points")

    main(in_fc=feature_class)

# TODO: Check if updates need to be made for the uncorrelated Milliman data.
