from chaostoolkitfuzzdiscover.constants.tmpfilenames import backup_data_binary
from chaostoolkitfuzzdiscover.fuzzinternalfilereads.instrumentsource import restore_source_from_backup
import pickle

__binary_file = open(backup_data_binary, mode='r')
backup_data = pickle.load(__binary_file)
__binary_file.close()
restore_source_from_backup(backup_data)