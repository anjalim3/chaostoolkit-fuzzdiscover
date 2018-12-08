from chaostoolkitfuzzdiscover.fuzzfilereads.instrumentsource import restore_source_from_backup
import pickle

def restore_from_backup(backup_binary):
    __binary_file = open(backup_binary, mode='r')
    backup_data = pickle.load(__binary_file)
    __binary_file.close()
    restore_source_from_backup(backup_data)