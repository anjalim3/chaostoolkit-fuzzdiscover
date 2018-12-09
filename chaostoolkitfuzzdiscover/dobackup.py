from sourcebackup import SourceBackup
from chaostoolkitfuzzdiscover_steadystatehypothesis.filenames import backup_root
import os

def do_backup(application_source_file_urls):
    backup_files = SourceBackup()
    if not os.path.exists(backup_root):
       os.makedirs(backup_root)
    for index, source_file in enumerate(application_source_file_urls):
        new_source_file = "ct_fuzz_backup_"+str(index)+".backup"
        backup_files.add_file_to_backups(new_source_file, source_file)
        with open(str(source_file)) as original:
            with open(backup_root+new_source_file, "w") as backup:
                for line in original:
                    backup.write(line)
    return backup_files
