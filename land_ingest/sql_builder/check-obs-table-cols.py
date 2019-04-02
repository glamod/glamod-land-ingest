with open('obs_table_cols.txt') as r:
    dbcols = [x.strip().split()[0] for x in r]

cols = """observation_id|report_id|data_policy_licence|date_time|date_time_meaning|observation_duration|longitude|latitude|crs|z_coordinate|z_coordinate_type|observation_height_above_station_surface|observed_variable|secondary_variable|observation_value|value_significance|secondary_value|units|code_table|conversion_flag|location_method|location_precision|z_coordinate_method|bbox_min_longitude|bbox_max_longitude|bbox_min_latitude|bbox_max_latitude|spatial_representativness|quality_flag|numerical_precision|sensor_id|sensor_automation_status|exposure_of_sensor|original_precision|original_units|original_code_table|original_value|conversion_method|processing_code|processing_level|adjustment_id|traceability|advanced_qc|advanced_homogenisation|source_id|report_type|station_type|location""".split('|')
print(cols)
print(dbcols)

print(cols == dbcols)
