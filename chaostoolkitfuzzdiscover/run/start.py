from chaostoolkitfuzzdiscover.modelgenerator.inputparser import InputParser
from chaostoolkitfuzzdiscover.fuzzfilereads.instrumentsource import fuzzed_file_name
from chaostoolkitfuzzdiscover.restorebackup import store_into_backup
from chaostoolkitfuzzdiscover.constants.tmpfilenames import source_file_backup_data_binary, input_file_backup_data_binary, fuzz_Input_data_location, tmp_folder
from kitty.controllers import EmptyController
from kitty.fuzzers import ServerFuzzer
from kitty.interfaces import WebInterface
from katnip.targets.file import FileTarget
from kitty.model import String
from kitty.model import Template
from kitty.model import GraphModel
from chaostoolkitfuzzdiscover.experimentfilewriter.writegeneratedfuzz import InputFuzzExperimentGenerator, InputFileFuzzExperimentGenerator, InternalFileFuzzExperimentGenerator
import os, shutil, pickle


sample_template = Template(name='T1', fields=[
    String('The default string', name='S1_1'),
    String('Another string', name='S1_2'),
])
sample_model = GraphModel()
sample_model.connect(sample_template)
#TODO : Add input validations & fix input
def __generate_fuzz_file_for_fuzzinternalfilereads(input_files = None, sample_input = None):
    controller = EmptyController()
    __my_modal = sample_model
    __tmp_folder = tmp_folder
    if os.path.exists(__tmp_folder):
        shutil.rmtree(__tmp_folder)
    if not os.path.exists(__tmp_folder):
        os.makedirs(__tmp_folder)
    if sample_input is not None:
        __parent_tokens = []
        for __si in sample_input:
            __tokens = str(__si).split()
            if len(__tokens)>2:
                __parent_tokens.extend(__tokens[2:])
            elif len(__tokens) == 2:
                __parent_tokens.extend(__tokens[1:])
            else:
                __parent_tokens.extend(__tokens)
        __my_modal = InputParser.get_kitty_models_from_sample_input(__parent_tokens, False)
    target = FileTarget('FileTarget', __tmp_folder, 'fuzzed')
    target.set_controller(controller)
    fuzzer = ServerFuzzer()
    fuzzer.set_interface(WebInterface(port=26001))
    fuzzer.set_model(__my_modal)
    fuzzer.set_target(target)
    fuzzer.start()
    fuzzer.stop()

def __generate_fuzz_data(index, kitty_modal):
    controller = EmptyController()
    if os.path.exists(fuzz_Input_data_location):
        shutil.rmtree(fuzz_Input_data_location)
    if not os.path.exists(fuzz_Input_data_location):
        os.makedirs(fuzz_Input_data_location)
    target = FileTarget('FileTarget', fuzz_Input_data_location, 'fuzzed'+str(index))
    target.set_controller(controller)
    fuzzer = ServerFuzzer()
    fuzzer.set_interface(WebInterface(port=26001))
    fuzzer.set_model(kitty_modal)
    fuzzer.set_target(target)
    fuzzer.start()
    fuzzer.stop()

#Step 1: Parse input and generate a data modal
def chaostoolkit_fuzzexperiment_wInputFuzzing(__file_name):
    start_up, fuzz_internal_files, kitty_modals, backup_source_files, backup_input_files, __sample_input = InputParser.parse_userinput(__file_name, suppress_internal_file_fuzzing=True, suppress_input_file_fuzzing=True)
    for index, modal in enumerate(kitty_modals):
        __generate_fuzz_data(index, modal)
    __experiment_generator_obj = InputFuzzExperimentGenerator()
    __experiment_generator_obj.set_startup_scripts(start_up)
    __experiment_generator_obj.generate_experiment_json("_input_fuzz_only")

#Step 2: If any user has provided input files, then back them up
def chaostoolkit_fuzzexperiment_Input_File_Fuzzing(__file_name):
    start_up, fuzz_internal_files, kitty_modals, backup_source_files, backup_input_files, __sample_input = InputParser.parse_userinput(__file_name, suppress_input_fuzzing=True, suppress_internal_file_fuzzing=True)
    if backup_input_files is not None:
        store_into_backup(backup_input_files, input_file_backup_data_binary)
    __generate_fuzz_file_for_fuzzinternalfilereads(input_files=backup_input_files)
    __experiment_generator_obj = InputFileFuzzExperimentGenerator(backup_input_files.get_backup_files(), __sample_input)
    __experiment_generator_obj.set_startup_scripts(start_up)
    __experiment_generator_obj.generate_experiment_json("_input_file_fuzz_only")

#Step 3: If user has asked for fuzzing of internal file reads, back up the input files (because we will be modifying them)
def chaostoolkit_fuzzexperiment_Internal_File_Read_Fuzzing(__file_name):
    start_up, fuzz_internal_files, kitty_modals, backup_source_files, backup_input_files, __sample_input = InputParser.parse_userinput(__file_name, suppress_input_fuzzing=True, suppress_input_file_fuzzing=True)
    if backup_source_files is not None:
        store_into_backup(backup_source_files, source_file_backup_data_binary)
    __generate_fuzz_file_for_fuzzinternalfilereads(sample_input=__sample_input)
    __experiment_generator_obj = InternalFileFuzzExperimentGenerator(__sample_input)
    __experiment_generator_obj.set_startup_scripts(start_up)
    __experiment_generator_obj.generate_experiment_json("_internal_file_read_fuzz_only")
