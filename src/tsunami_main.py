"""
Filename: tsunami_main.py
Purpose: Main script to process the data.
Author: Jesse Morgan
Date: 5/27/2026
Updates: None
"""
import csv
import os
import sys
from pathlib import Path
import clip_feature_class
import convert_from_csv
import convert_to_csv
import create_fields
import create_file_gdb
import extract_fips_county_name
import populate_first_floor
import populate_found_type_id
import extract_census_tract
import populate_building_deduct
import populate_building_limit
import populate_cb_fips
import populate_content_deduct
import populate_content_limits
import populate_eq_bldg_type
import populate_eq_design_level
import populate_geometry
import populate_id
import populate_lat_lon
import populate_lmh_rise_and_bldg_ht
import populate_per_sq_ft_avg_val
import populate_pop_fields
import populate_occupancy_type
import populate_site_elevation
import populate_socc_type_id
import populate_val_cont
import populate_val_struct

# These are the fields from the latest Milliman data received
REQUIRED_CSV_FIELDS = ["location", "BLDG_DED", "BLDG_LIMIT", "CNT_DED", "CNT_LIMIT",
                       "STATE", "POSTCODE", "COUNTRY", "LON", "LAT", "BLDG_VALUE",
                       "CNT_VALUE", "CONSTR_CODE", "NUM_STORIES", "YEAR_BUILT",
                       "foundationtype", "BasementFinishType", "FIRST_FLOOR_ELEV",
                       "BASE_FLOOD_ELEV", "elev_ft"]

def main(in_csv, out_folder, tsunami_polygon, hazus_counties, census_tract_data, census_blocks_data):
    """
    Main processing function.

    Parameters:
        in_csv - Path to the CSV file to process.
        out_folder - Path the output folder.
        tsunami_polygon - Path the Tsunami clipping polygon.
        hazus_counties - Path the County data from Hazus
        census_tract_data - Path to the Census Tract feature class.
        census_blocks - Path the Census Block feature class.

    Returns:
        None
    """
    # Get the CSV name
    csv_name = os.path.basename(in_csv)

    # Get the first row of the CSV to verify all the needed columns exists.
    with open(in_csv, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        first_row = next(reader)

    # Verify the column names exists
    print("Checking for required columns in the CSV...")
    for required_column in REQUIRED_CSV_FIELDS:
        if required_column not in first_row:
            print(f"ERROR: The field {required_column} is missing.")
            sys.exit(1)

    # Create the file geodatabase
    print("Creating the file geodatabase...")
    file_gdb_path = create_file_gdb.main(
        folder_path=out_folder,
        gdb_name=csv_name.replace(".csv", ""))

    # Convert the CSV to a feature class
    print("Converting CSV...")
    fc_name = convert_from_csv.main(file_gdb_path=file_gdb_path, csv_path=in_csv)

    # Clip the feature class to the tsunami polygons
    print("Clipping points...")
    clipped_fc_name = clip_feature_class.main(
       in_fc=os.path.join(file_gdb_path, fc_name),
       tsunami_polygon=tsunami_polygon)

    # Create a full path to the Points
    fc_path = str(os.path.join(file_gdb_path, clipped_fc_name))

    # Add the required fields to the feature class
    print("Adding required fields...")
    create_fields.main(in_fc=fc_path)

    # Get the FIPs and County Name for each point
    print("Extracting FIPS and County Names...")
    extract_fips_county_name.main(in_fc=fc_path, hazus_counties=hazus_counties)

    # Get the Census Tract for each point
    print("Extracting Census Tract...")
    extract_census_tract.main(in_fc=fc_path, census_tract_data=census_tract_data)

    # Get the Census Block ID for each point
    print("Populate the CBFips field..")
    populate_cb_fips.main(in_fc=fc_path, census_blocks=census_blocks_data)

    # Populate the ID field
    print("Populating the ID field...")
    populate_id.main(in_fc=fc_path)

    # Populate the SiteElevation_UserDefined_ft field
    print("Populating the SiteElevation_UserDefined_ft field...")
    populate_site_elevation.main(in_fc=fc_path)

    # Populate the Building Limit fields
    print("Populating the Building Limit fields...")
    populate_building_limit.main(in_fc=fc_path)

    # Populate the Content Limit fields
    print("Populating the Content Limit fields...")
    populate_content_limits.main(in_fc=fc_path)

    # Populate the Building Deductible fields
    print("Populating the Building Deductible fields...")
    populate_building_deduct.main(in_fc=fc_path)

    # Populate the Content Deductible fields
    print("Populating the Content Deductible fields...")
    populate_content_deduct.main(in_fc=fc_path)

   # Populate the SOccTypeID field
    print("Populating the SOccTypeID field...")
    populate_socc_type_id.main(in_fc=fc_path)

   # Populate the FoundTypeID field
    print("Populating the FoundTypeID field...")
    populate_found_type_id.main(in_fc=fc_path)

    # Populate the FirstFloor field
    print("Populating the FirstFloor field...")
    populate_first_floor.main(in_fc=fc_path)

    # Populate the ValStruct field
    print("Populating the ValStruct field...")
    populate_val_struct.main(in_fc=fc_path)

    # Populate the ValCont field
    print("Populating the ValCont field...")
    populate_val_cont.main(in_fc=fc_path)

    # Populate the LMH_Rise and Building Height fields
    print("Populating the LMH_Rise and Building Height fields...")
    populate_lmh_rise_and_bldg_ht.main(in_fc=fc_path)

    # Populate the Occupancy_Type
    print("Populating the Occupancy_Type field...")
    populate_occupancy_type.main(in_fc=fc_path)

    # Populate the PerSqftAvgVal field
    print("Populating the PerSqftAvgVal field...")
    populate_per_sq_ft_avg_val.main(in_fc=fc_path)

    # Populate the Earthquake Building Types field
    print("Populating the Earthquake Building Types fields...")
    populate_eq_bldg_type.main(in_fc=fc_path)

    # Populate the EqDesignLe field
    print("Populating the EqDesignLe field...")
    populate_eq_design_level.main(in_fc=fc_path)    

    # Populate the Population fields
    print("Populating the Population fields...")
    populate_pop_fields.main(in_fc=fc_path)

    # Populate the Latitude and Longitude fields
    print("Populating the Latitude and Longitude fields...")
    populate_lat_lon.main(in_fc=fc_path)

    # Populate the Geometry field
    print("Populating the Geometry field...")
    populate_geometry.main(in_fc=fc_path)

    # Output the CSV
    print("Exporting the CSV...")
    convert_to_csv.main(in_fc=fc_path, output_folder=output_folder)

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    data_folder = os.path.join(script_dir.parent, "data")
    output_folder = os.path.join(script_dir.parent, "outputs")
    hazus_counties_fc = os.path.join(data_folder, "Hazus_Data.gdb\\Counties")
    census_pop_fc = os.path.join(data_folder, "Census_Data.gdb\\Census_Tract_Population")
    census_blocks = os.path.join(data_folder, "Census_Data.gdb\\Census_Blocks")
    tsunami_fc = os.path.join(data_folder, "ASCE_Tsunami_Design_Zones.gdb\\ts2022_Tsunami_Design_Zone_Clipped_To_Shoreline")

    csv_files = [
        "AK_ucmb.csv", 
        "AK_uni.csv",
        "CA_ucmb.csv",
        "CA_uni.csv",
        "HI_ucmb.csv",
        "HI_uni.csv", 
        "OR_ucmb.csv",
        "OR_uni.csv", 
        "WA_ucmb.csv",
        "WA_uni.csv"
    ]

    for csv_file in csv_files:
        print(f"Processing {csv_file}...")
        print("--------------------------------------------------------")
        main(in_csv=os.path.join(data_folder, csv_file),
            out_folder=output_folder,
            tsunami_polygon=tsunami_fc,
            hazus_counties=hazus_counties_fc,
            census_tract_data=census_pop_fc,
            census_blocks_data=census_blocks)        
        print("...done")
        print("--------------------------------------------------------\n")
