"""
Filename: max_min_field_values.py
Purpose: Find the maximum and minimum values of a field in a feature class.
Author: Jesse Morgan
Date: 5/29/2026
Updates: None

Note: This tool is only used for describing the data.  It's not used for the analysis.
      It's ran from ArcToolbox.
"""
import arcpy
import sys

feature_class = sys.argv[1]
field_name = sys.argv[2]

with arcpy.da.SearchCursor(feature_class, [field_name]) as cursor:
    max_value = max([row[0] for row in cursor if row[0] is not None])

with arcpy.da.SearchCursor(feature_class, [field_name]) as cursor:    
    min_value = min([row[0] for row in cursor if row[0] is not None])

arcpy.AddMessage(f"The maximum value is: {max_value}")
arcpy.AddMessage(f"The minimum value is: {min_value}")