"""
Filename: populate_eq_bldg_type.py
Purpose: Populate Earthquake Building Type ID (EqBldgType) field and EdgBldgTypeClass fields
Author: Jesse Morgan
Date: 5/28/2026
Updates: None

Note: Scope of work only includes California, Oregon, Washington, Alaska and Hawaii.

Note: Code is only written for MDI data.

Note: The only 'CONSTR_CODE' values found were 1 = frame and 2 = masonry
      The only 'NUM_STORIES' values found were 1, 2, and 3.
"""
import os
import sys
from pathlib import Path
import arcpy


def calc_w1(in_fc):
    """
    Populate the Earthquake Building Type of W1
        EqBldgType = 1
        eqBldgType   = W1
        General      = Wood
        Description  = Wood, Light Frame (< 5,000 sq. ft.)

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    construction_type = arcpy.AddFieldDelimiters(in_fc, "CONSTR_CODE")
    stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")
    areaSqFt = arcpy.AddFieldDelimiters(in_fc, "AreaSqft")

    # Create the SQL expression to select the rows.
    sql_exp = f"{construction_type} = 1 AND  {stories} <= 2 AND {areaSqFt} < 5000"

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqBldgType for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqBldgType",
            expression="1",
            expression_type="PYTHON3")

        # Calculate the EdgBldgTypeClass for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EdgBldgTypeClass",
            expression="'W1'",
            expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_w2(in_fc):
    """
    Populate the Earthquake Building Type of W2
        EqBldgType = 2
        eqBldgType   = W2
        General      = Wood
        Description  = Wood, Commercial and Industrial Wood (>5,000 sq. ft.)

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    construction_type = arcpy.AddFieldDelimiters(in_fc, "CONSTR_CODE")
    areaSqFt = arcpy.AddFieldDelimiters(in_fc, "AreaSqft")

    # Create the SQL expression to select the rows.
    sql_exp = f"{construction_type} = 1 AND {areaSqFt} >= 5000"

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqBldgType for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqBldgType",
            expression="2",
            expression_type="PYTHON3")

        # Calculate the EdgBldgTypeClass for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EdgBldgTypeClass",
            expression="'W2'",
            expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_w31(in_fc):
    """
    Populate the Earthquake Building Type of W31
        EqBldgType = 31
        eqBldgType   = RM2L
        General      = Masonry
        Description  = Reinforced Masonry Bearing Walls with Precast Concrete Diaphragms Low-Rise

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    construction_type = arcpy.AddFieldDelimiters(in_fc, "CONSTR_CODE")
    stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")
    year_built = arcpy.AddFieldDelimiters(in_fc, "YEAR_BUILT")

    # Create the SQL expression to select the rows.
    sql_exp = f"{construction_type} = 2 AND " \
              f"{stories} <= 3 AND " \
              f"{year_built} > 1974"

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqBldgType for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqBldgType",
            expression="31",
            expression_type="PYTHON3")

        # Calculate the EdgBldgTypeClass for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EdgBldgTypeClass",
            expression="'RM2L'",
            expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_w34(in_fc):
    """
    Populate the Earthquake Building Type of W34
        EqBldgType = 34
        eqBldgType   = URML
        General      = Masonry
        Description  = Unreinforced Masonry Bearing Walls Low-Rise

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    construction_type = arcpy.AddFieldDelimiters(in_fc, "CONSTR_CODE")
    stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")
    year_built = arcpy.AddFieldDelimiters(in_fc, "YEAR_BUILT")

    # Create the SQL expression to select the rows.
    sql_exp = f"{construction_type} = 2 AND " \
              f"{stories} <= 2 AND " \
              f"{year_built} <= 1974"

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqBldgType for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqBldgType",
            expression="34",
            expression_type="PYTHON3")

        # Calculate the EdgBldgTypeClass for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EdgBldgTypeClass",
            expression="'URML'",
            expression_type="PYTHON3")

    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        sys.exit(1)

def calc_w35(in_fc):
    """
    Populate the Earthquake Building Type of W35
        EqBldgType = 35
        eqBldgType   = URMM
        General      = Masonry
        Description  = Unreinforced Masonry Bearing Walls Mid-Rise

    Arguments:
        in_fc - The feature class to update.

    Returns:
        None
    """
    # Create field deliminators based on the data source.
    construction_type = arcpy.AddFieldDelimiters(in_fc, "CONSTR_CODE")
    stories = arcpy.AddFieldDelimiters(in_fc, "NUM_STORIES")
    year_built = arcpy.AddFieldDelimiters(in_fc, "YEAR_BUILT")

    # Create the SQL expression to select the rows.
    sql_exp = f"{construction_type} = 2 AND " \
              f"{stories} = 3 AND " \
              f"{year_built} <= 1974"

    try:
        # Select the rows.
        selected_rows = arcpy.management.SelectLayerByAttribute(
            in_layer_or_view=in_fc,
            selection_type="NEW_SELECTION",
            where_clause=sql_exp)

        # Calculate the EqBldgType for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EqBldgType",
            expression="35",
            expression_type="PYTHON3")

        # Calculate the EdgBldgTypeClass for the selected rows.
        arcpy.management.CalculateField(
            in_table=selected_rows,
            field="EdgBldgTypeClass",
            expression="'URMM'",
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
    calc_w1(in_fc=in_fc)
    calc_w2(in_fc=in_fc)
    calc_w31(in_fc=in_fc)
    calc_w34(in_fc=in_fc)
    calc_w35(in_fc=in_fc)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    out_folder = os.path.join(script_dir.parent, "outputs")
    feature_class = os.path.join(out_folder, "or_uni.gdb\\or_uni_points")

    main(in_fc=feature_class)

# TODO: Add more building types as needed. The uncorrelated update is adding two more construction types to the dataset, 
#       there will be five in total: frame, masonry, concrete, steel, mobile home