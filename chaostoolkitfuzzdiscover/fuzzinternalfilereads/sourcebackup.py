class SourceBackup:
    __source_backups = None

    def __init__(self):
        self.__source_backups = []

    def add_file_to_backups(self, backup_file, original_file):
        self.__source_backups.append({"backup": backup_file, "original": original_file})

    def get_backup_files(self):
        return self.__source_backups
