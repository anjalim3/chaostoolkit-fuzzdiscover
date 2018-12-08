from sourcebackup import SourceBackup
import re

#ToDo: fix issue with paths from home
#ToDo: fix need to create directories
__python_regex_part_1 = "((open\(.+?,'r'\))|(open\(.+?\))|"
__python_regex_part_2 = '(open\(.+?,\\\"r\\\"\)))'
__generic_delimiters_begin = ""#" |\t|\n" #[" ", "\t", "\n"]
__generic_delimiters_end = ""#" |\t|\n"#[" ", "\t", "\n"]
__python_delimiters_end = ""#":|\\\\"#[":", "\\\\"]
fuzzed_file_name = "'../../fuzzed_file.txt'"
__back_up_dir = "../../backup/"

def __unsupported_file_type(backup_file, sourcefile):
    raise Exception("Unsupported file type for source file: "+sourcefile)

#ToDo: this method is incomplete. broken regex.
def __mock_file_reads_in_python(backup_file, source_file):
    __regex = __python_regex_part_1 + __python_regex_part_2  # + "(" + __generic_delimiters_end + "|" + __python_delimiters_end + ")"
    with open(__back_up_dir+str(backup_file), 'r') as __original_read:
        with open(str(source_file), 'w') as __original_write:
            for line in __original_read:
                line = re.sub(__regex,  "open(" + fuzzed_file_name + ",'r')", line)
                __original_write.write(line)

def __mock_file_reads_in_source(backup_files):
    for backup in backup_files.get_backup_files():
        __index_of_file_extension = str(backup['original']).rfind(".")
        __file_extension = str(backup['original'])[__index_of_file_extension+1:]
        func =__mock_file.get(__file_extension, lambda __lambda_backup, __lambda_source: __unsupported_file_type(__lambda_backup, __lambda_source))
        func(str(backup['backup']), str(backup['original']))

def instrument_source(application_source_file_urls, is_source_file):
    backup_files = SourceBackup()
    for index, source_file in enumerate(application_source_file_urls):
        new_source_file = "ct_fuzz_backup_"+str(index)+".backup"
        backup_files.add_file_to_backups(new_source_file, source_file)
        with open(str(source_file)) as original:
            with open("../../backup/"+new_source_file, "w") as backup:
                for line in original:
                    backup.write(line)
    if is_source_file:
        __mock_file_reads_in_source(backup_files)
    return backup_files

def restore_source_from_backup(backup_files):
    if not isinstance(backup_files, SourceBackup):
        raise ValueError("Incorrect object for backup_files. The object much be an instance of SourceBackup")
    __backup_files_list = backup_files.get_backup_files()
    for __backup_data in __backup_files_list:
        __backup = __backup_data['backup']
        __original = __backup_data['original']
        with open(str("../../backup/"+__backup),'r') as __backup_file:
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
