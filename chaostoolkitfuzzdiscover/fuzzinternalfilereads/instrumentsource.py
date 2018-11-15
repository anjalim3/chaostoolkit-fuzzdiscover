from sourcebackup import SourceBackup

#ToDo: fix issue with paths from home
#ToDo: fix need to create directories

def __unsupported_file_type(sourcefile):
    raise Exception("Unsupported file type for source file: "+sourcefile)

def __mock_file_reads_in_python(source_file):
    with open(str(source_file)) as original:
        for line in original:
            original.write(line.replace("fopen"))
            print line
            #TODO: Replace fopen(something, r) with fopen("fuzzed_file", r). But it's 3:30 am and I want to sleep now


def __mock_file_reads_in_source(application_source_file_urls):
    for source_file in application_source_file_urls:
        __index_of_file_extension = str(source_file).rfind(".")
        __file_extension = str(source_file)[__index_of_file_extension+1:]

def instrument_source(application_source_file_urls):
    backup_files = SourceBackup()
    for source_file in application_source_file_urls:
        if "/" in source_file:
            __last_index = str(source_file).rfind("/")
            truncated_source_file_name = str(source_file)[__last_index+1:]
        else:
            truncated_source_file_name = source_file
        new_source_file = "ct_fuzz_"+truncated_source_file_name
        backup_files.add_file_to_backups(new_source_file, source_file)
        with open(str(source_file)) as original:
            with open("../../backup/"+new_source_file, "w") as backup:
                for line in original:
                    backup.write(line)
        __mock_file_reads_in_source(application_source_file_urls)
        return backup_files

def restore_source_from_backup(backup_files):
    if not isinstance(backup_files, SourceBackup):
        raise ValueError("Incorrect object for backup_files. The object much be an instance of SourceBackup")
    __backup_files_list = backup_files.get_backup_files()
    for __backup, __original in __backup_files_list:
        with open(str("../../backup/"+__backup)) as __backup_file:
            with open(__original, "w") as __original_file:
                for line in __backup_file:
                    __original_file.write(line)

#ToDo: add support for other languages
__mock_file = {
    "py" : __mock_file_reads_in_python,
    "c"  : __unsupported_file_type,
    "c++": __unsupported_file_type,
    "java": __unsupported_file_type
}
