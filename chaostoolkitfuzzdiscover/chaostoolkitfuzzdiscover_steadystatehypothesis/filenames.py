chaostoolkit_fuzzdicover_root = '/tmp/chaostoolkit-fuzzdiscover/'
probe_file_destination = chaostoolkit_fuzzdicover_root+'probes/'
probe_start_indicator = probe_file_destination+'DO_NOT_DELETE_start_indicator'
final_top_cmd_dump = probe_file_destination+'final_top_dump'
initial_top_cmd_dump = probe_file_destination+'initial_top_dump'
initial_df_cmd_dump = probe_file_destination+'initial_df_dump'
final_df_cmd_dump = probe_file_destination+'final_df_dump'
fuzz_Input_data_location = chaostoolkit_fuzzdicover_root + 'output/'
mysql_conn_pool_status = probe_file_destination+'mysql_connpool_status'
backup_root = chaostoolkit_fuzzdicover_root + 'backup/'
source_file_backup_data_binary = backup_root+'pickled_source_file_backup_data.bin'
input_file_backup_data_binary = backup_root+'pickled_input_file_backup_data.bin'