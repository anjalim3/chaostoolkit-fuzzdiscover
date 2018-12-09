import json
import os
from chaostoolkitfuzzdiscover_steadystatehypothesis.filenames import backup_root

def restore_from_backup(backup_binary):
    __binary_file = open(backup_binary, mode='r')
    backup_data = json.load(__binary_file)
    __binary_file.close()
    restore_source_from_backup(backup_data['pickle'])

def store_into_backup(backup_source_files, source_file_backup_data_binary):
    __clone = {}
    __clone["pickle"] = backup_source_files.get_backup_files()
    __binary_file = open(source_file_backup_data_binary, mode='w')
    json.dump(__clone, __binary_file)
    __binary_file.close()

def restore_source_from_backup(backup_files):
    for __backup_data in backup_files:
        __backup = __backup_data['backup']
        __original = __backup_data['original']
        os.system("cp "+backup_root+__backup+" "+__original)