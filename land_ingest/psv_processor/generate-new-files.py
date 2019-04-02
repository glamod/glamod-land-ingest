import pandas as pd
import argparse
import sys
import os
import re
import datetime as dt
from collections import OrderedDict
from pandas.testing import assert_frame_equal



BASE_PATH = '/gws/nopw/j04/c3s311a_lot2/data/glamod_land_delivery_2018_12_31_Beta/'
FIXED_PATH = '/gws/nopw/j04/c3s311a_lot2/data/beta_fix7/'
STATION_FILE = BASE_PATH + 'station_configuration/station_configuration_Beta.psv'
TEST_MODE = False


def parse_args():
 
    parser = argparse.ArgumentParser(description='Fix land data')

    parser.add_argument('-index', dest='idx', type=int, required=True, help='Job index number')
    parser.add_argument('-header_file_count', dest='header_file_count', type=int, required=True, help='Header files to process')
    parser.add_argument('-n_parallel_jobs', dest='n_parallel_jobs', type = int, required=True, help='Number of parallel jobs to run on LOTUS')

    args = parser.parse_args()
    return args


def check_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)


def get_station_configuration_table():

    # Load station configuration file (all columns as object to avoid type promotion)
    # Read in station config file, this only needs to be done once
    station_configuration = pd.read_csv(STATION_FILE, sep='|', dtype=object)

    if 'source_id ' in station_configuration.columns:
        station_configuration = station_configuration.rename({'source_id ': 'source_id'})

    station_configuration['source_id'] = station_configuration['source_id'].apply(lambda x: x.strip())

    # rename record_number to station_record_number
    station_configuration = station_configuration.rename(columns={
        'record_number': 'station_record_number',
        'primary_id':'primary_station_id'})

    return station_configuration



def main():

    station_configuration = get_station_configuration_table()

#    TEST_MODE = True

    # Run in test mode if file_list is defined
    if TEST_MODE:
        test_file = 'header_table/monthly/header_table_BETA_USW00003867_1.psv'
        file_list = [test_file]
        file_idx = [0]

    else:
        args = parse_args() 
        file_idx = range(args.idx - 1, args.header_file_count, args.n_parallel_jobs)

        with open('header_table_files.txt') as f:
            file_list = [i.strip() for i in f.readlines()]

    COUNTER = 0
    for idx in file_idx:

        COUNTER += 1

        # Uncomment next line to stop after one iteration
        if TEST_MODE and COUNTER > 1: return
 
        header_file = file_list[idx]

        # get ID from header file name
        filename = os.path.basename(header_file)
        station_id = re.match('^header_table_BETA_(.+)_\d+\.psv', filename).groups()[0]

        # Get observations file based on header file
        observation_file = header_file.replace('header_table', 'observations_table')
        observation_file = observation_file.replace('observations_table_BETA', 'observation_table_BETA')
        print('Processing: ' + header_file)

        # Load header table (all object) 
        # E.g.: header_file = 'header_table/daily/T3_protect/header_table_BETA_SWE00139284_1.psv'
        header_path = BASE_PATH + header_file

        header_table = pd.read_csv(header_path, sep='|', dtype=object)

        if len(header_table) == 0:
            print('[WARNING] No records in header table so exiting: {}'.format(header_path))
            continue

        print('Header file: {}'.format(header_path))

        if 'source_id ' in header_table.columns:
            header_table = header_table.rename(columns = {'source_id ': 'source_id'})

        # header table has extraneous space at end of source_id field, remove
        header_table['source_id'] = header_table['source_id'].apply(lambda x: x.strip())

        if 'report_meaning_of_time_stamp' in header_table.columns:
            header_table = header_table.rename(columns={'report_meaning_of_time_stamp': 'report_meaning_of_timestamp'})

        # load observations table (all object)
        # E.g.: observation_file = '/observations_table/daily/T3_protect/observation_table_BETA_SWE00139284_1.psv'
        observations_path = BASE_PATH +  observation_file
        print('Observations file: {}'.format(observations_path))

        observations_table = pd.read_csv(observations_path, sep='|', dtype=object)

        if len(observations_table) == 0:
            print('[WARNING] No records in observations table so exiting: {}'.format(observations_path))
            continue

        if 'source_id ' in observations_table.columns:
            observations_table = observations_table.rename(columns={'source_id ': 'source_id'})

        # observations table has extraneous space at end of source_id field, remove
        observations_table['source_id'] = observations_table['source_id'].apply(lambda x: x.strip())

        # Select row(s) from Source Configuration that match station id and record number
        station_config_subset = station_configuration.loc[(station_configuration['primary_station_id'] == station_id)].copy()

        if len(station_config_subset) == 0:
            raise Exception('Cannot find station ID in Source Configuration: {}'.format(station_id, record_number))

        ot = observations_table
        ht = header_table
        scs = station_config_subset

        # Check that 'source_id' is same in station_configuration, header_table and observations_table
#        if len(header_table['source_id'].unique()) > 
         
        try:
            scs_ids = set([int(src) for src in station_config_subset['source_id']])
            ht_ids = set([int(src) for src in header_table['source_id'].unique()])
            ot_ids = set([int(src) for src in observations_table['source_id'].unique()])

            if (not ht_ids.issubset(scs_ids)) or (not ot_ids.issubset(scs_ids)):

                assert(len(scs_ids) == 1)
                src_id = scs_ids[0]

                # Make an exception for monthly files - overwrite "source_id" using Station Config value
                if "/monthly/" in header_path:
                    print('[INFO] Overwriting "source_id" using Station Configuration value in Header/Obs tables: {}'.format(src_id))
                    header_table['source_id'] = str(src_id)
                    observations_table['source_id'] = str(src_id)
                else:
                    assert(ht_ids.issubset(scs_ids) and ot_ids.issubset(scs_ids))
        except Exception as err:
            print('[ERROR] Cannot match "source_id" in files:')
            print('        {} :: {}'.format(scs_ids, STATION_FILE))
            print('        {} :: {}'.format(ht_ids, header_path))
            print('        {} :: {}'.format(ot_ids, observations_path))
            continue

        # Before merge of Header table and Station Configuration subset, check they will merge properly
        if not set(header_table['station_record_number']).intersection(set(station_config_subset['station_record_number'])):
            print('[WARNING] No valid merge between Header and Station Config tables on: "station_record_number". {}'.format(header_path))
            continue

        # merge tables
        master_table = header_table.merge(station_config_subset, how='left',
                                          on=['primary_station_id', 'station_record_number'],
                                          suffixes=('_head','_station'))

        mt = master_table

        if pd.np.nan in list(mt['longitude'].unique()) or pd.np.nan in list(mt['latitude'].unique()):
            print('[WARNING] NANs in master table "longitude" or "latitude"! {}'.format(header_path))
            continue

        # Rename to 'source_id' so we can join on that and 'report_id'
        master_table = master_table.rename(columns={'source_id_station': 'source_id'})

        # merge observation and header table
        master_table = master_table.merge(observations_table, how='outer',
                                          on=['report_id'], suffixes=('', '_obs'))

        # check we have data
        if master_table.shape[0] == 0:
            print('[WARNING] Master table has no content: {}'.format(header_path))
            continue

        # rename master columns
        master_table = master_table.rename(columns={
#            'source_id_station': 'source_id',
            'data_policy_licence_station': 'data_policy_licence',
            'station_crs': 'crs',
            'operating_territory': 'sub_region'
        })

        # Filter out any records without an observation_id - they will never work
        print('[WARNING] Filtering out any master table records without an Observation ID')
        master_table = master_table.loc[master_table['observation_id'].notnull()] 
        
        if 'sub_daily' in header_file:
            report_type = 0  # SYNOP
        elif 'daily' in header_file:
            report_type = 3  # DAILY
        elif 'monthly' in header_file:
            report_type = 2  # CLIMAT
        else:
            raise ('Error, bad report_type')

        master_table['report_type'] = report_type

        # null columns to add
        master_table = master_table.assign(station_speed = '')
        master_table = master_table.assign(station_course = '')
        master_table = master_table.assign(station_heading = '')
        master_table = master_table.assign(source_record_id = '')
        master_table = master_table.assign(secondary_variable = '')
        master_table = master_table.assign(code_table = '')
        master_table = master_table.assign(z_coordinate_method = '')
        master_table = master_table.assign(sensor_id = '')
        master_table = master_table.assign(sensor_automation_status = '')
        master_table = master_table.assign(exposure_of_sensor = '')
        master_table = master_table.assign(original_code_table = '')
        master_table = master_table.assign(processing_code = '')
        master_table = master_table.assign(adjustment_id = '' )
        master_table = master_table.assign(traceability = '')
        master_table = master_table.assign(advanced_qc = '')
        master_table = master_table.assign(advanced_uncertainty = '')
        master_table = master_table.assign(advanced_homogenisation = '')
        master_table = master_table.assign(z_coordinate = '')
        master_table = master_table.assign(z_coordinate_type = '')
        master_table = master_table.assign(spatial_representativeness = '')

        # add location column
        location = master_table.apply(lambda x: 'SRID=4326;POINT({0} {1})'.format(x['longitude'], x['latitude']), axis = 1)
        master_table = master_table.assign(location=location)

        # replace array fields with {} (all empty for beta release)
        master_table['application_area'] = '{}'
        master_table['observing_programme'] = '{}'
        master_table['events_at_station'] = '{}'
        master_table['duplicates'] = '{}'
        master_table['processing_codes'] = '{}'

        master_table = master_table.replace('', 'NULL')
        master_table = master_table.fillna('NULL')

        print('[INFO] Table sizes: Master = {}, Header = {}, Obs = {}'.format(len(master_table), len(ht), len(ot)))

        # add location to header table
        # write out new files
        header_columns = [
            'report_id','region', 'sub_region', 'application_area', 'observing_programme', 'report_type',
            'station_name','station_type','platform_type','platform_sub_type','primary_station_id','station_record_number',
            'primary_station_id_scheme','longitude','latitude','location_accuracy','location_method','location_quality',
            'crs','station_speed','station_course','station_heading','height_of_station_above_local_ground',
            'height_of_station_above_sea_level', 'height_of_station_above_sea_level_accuracy', 'sea_level_datum',
            'report_meaning_of_timestamp','report_timestamp','report_duration','report_time_accuracy','report_time_quality',
            'report_time_reference','profile_id','events_at_station','report_quality','duplicate_status','duplicates',
            'record_timestamp','history','processing_level','processing_codes','source_id','source_record_id','location'
        ]

        # add report_type, station_type and location to observations table
        observation_columns = [
            'observation_id','report_id','data_policy_licence','date_time','date_time_meaning','observation_duration',
            'longitude','latitude','crs','z_coordinate','z_coordinate_type','observation_height_above_station_surface',
            'observed_variable','secondary_variable','observation_value','value_significance','secondary_value','units',
            'code_table','conversion_flag','location_method','location_accuracy','z_coordinate_method','bbox_min_longitude',
            'bbox_max_longitude','bbox_min_latitude','bbox_max_latitude','spatial_representativeness','quality_flag',
            'numerical_precision','sensor_id','sensor_automation_status','exposure_of_sensor','original_precision',
            'original_units','original_code_table','original_value','conversion_method','processing_code','processing_level',
            'adjustment_id','traceability','advanced_qc','advanced_uncertainty','advanced_homogenisation','source_id',
            'report_type','station_type','location'
        ]


        # Construct and write header file (by year)
        header_table_out = master_table[header_columns].copy()
        header_path_new = FIXED_PATH + header_file
        write_outputs_by_year(header_table_out, header_path_new, input_file=header_path)

        # Construct and write observations file (by year)
        observations_table_out = master_table[observation_columns].copy()
        observations_table_out = observations_table_out.rename(columns = {'location_accuracy': 'location_precision'})
        observations_path_new = FIXED_PATH + observation_file
        write_outputs_by_year(observations_table_out, observations_path_new, input_file=observations_path)
    

def write_outputs_by_year(df, output_file_base, input_file):

    fdir, fname = os.path.split(output_file_base)

    # Drop duplicates in table
    df.drop_duplicates(inplace=True)

    # Get year range and then split DataFrame into years and write each year 
    # to file: "<base_name>.<year>.psv"
  
    # First: convert field to datetime
    if fname.startswith('header_table_'):
        time_field = 'report_timestamp'
        sort_fields = ['report_id', time_field]
        table_type = 'Header'
    else:
        time_field = 'date_time'
        sort_fields = ['observation_id', time_field]
        table_type = 'Observations'

    try:
        df[time_field] = pd.to_datetime(df[time_field], utc=True)
    except Exception as err:
        print('df[time_field] = pd.to_datetime(df[time_field], utc=True)')
#        import pdb; pdb.set_trace() 
        raise Exception('Failed to find valid time field: {}\nReview file: {}'.format(time_field, input_file))

    # Now work with time series from that field
    time_series = df[time_field]
    start_year = time_series.min().year
    end_year = time_series.max().year

    # Set up some temporary lists to check consistency
    dfs = OrderedDict()
    record_count = 0

    for year in range(start_year, end_year + 1):
#        print('[INFO] Filter by year: {}'.format(year))
        _df = df[df[time_field].dt.year == year]

        record_count += len(_df)
        dfs[year] = _df

    print('[INFO] Checking original Table matches those split by time...')
    if record_count != len(df):
        raise Exception('Split of records did not match original table size, for: {}'.format(output_file_base))

    # Test that the original data matches the split data (when sorted by time field)
    remade_df = pd.concat(dfs.values())
    remade_df.sort_values(sort_fields, inplace=True)
    df_sorted = df.sort_values(sort_fields)

    print('[WARNING] Frame sizes: remade_df: {}, df_sorted (orig): {}'.format(len(remade_df), len(df_sorted)))

    try:
        assert_frame_equal(df_sorted, remade_df)
    except Exception as err:
        raise Exception('Remade data frame does not match original, for: {}'.format(output_file_base))


    # Make sure output directory exists
    output_dir = os.path.join(fdir, fname.replace('.psv', ''))
    check_path(output_dir)

    # Now loop through each and write out
    for year, _df in dfs.items():

        # Ignore empty years
        if len(_df) == 0: continue

        fname_year = fname.replace('.psv', '.{}.psv'.format(year))
        out_path = os.path.join(output_dir, fname_year)

        _df.to_csv(out_path, sep='|', index=False, date_format='%Y-%m-%d %H:%M:%S%z')
        print('[INFO] {} file saved to: {}'.format(table_type, out_path))



if __name__ == '__main__':

    main()
