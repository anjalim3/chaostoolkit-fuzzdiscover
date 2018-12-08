from chaostoolkitfuzzdiscover.modelgenerator.inputparser import InputParser
from chaostoolkitfuzzdiscover.fuzzfilereads.instrumentsource import fuzzed_file_name
from chaostoolkitfuzzdiscover.constants.tmpfilenames import source_file_backup_data_binary, input_file_backup_data_binary, fuzz_Input_data_location, tmp_folder
from kitty.controllers import EmptyController
from kitty.fuzzers import ServerFuzzer
from kitty.interfaces import WebInterface
from katnip.targets.file import FileTarget
from kitty.model import String
from kitty.model import Template
from kitty.model import GraphModel
from chaostoolkitfuzzdiscover.experimentfilewriter.writegeneratedfuzz import ExperimentGenerator
import os, shutil, pickle


sample_template = Template(name='T1', fields=[
    String('The default string', name='S1_1'),
    String('Another string', name='S1_2'),
])
sample_model = GraphModel()
sample_model.connect(sample_template)
#TODO : Add input validations & fix input
def __generate_fuzz_file_for_fuzzinternalfilereads():
    controller = EmptyController()
    __tmp_folder = tmp_folder
    if os.path.exists(__tmp_folder):
        shutil.rmtree(__tmp_folder)
    if not os.path.exists(__tmp_folder):
        os.makedirs(__tmp_folder)
    target = FileTarget('FileTarget', __tmp_folder, 'fuzzed')
    target.set_controller(controller)
    fuzzer = ServerFuzzer()
    fuzzer.set_interface(WebInterface(port=26001))
    fuzzer.set_model(sample_model)
    fuzzer.set_target(target)
    fuzzer.start()
    fuzzer.stop()

def __generate_fuzz_data(index, kitty_modal):
    controller = EmptyController()
    #ToDo: fix need for manually creating output folder
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
start_up, fuzz_internal_files, kitty_modals, backup_source_files, backup_input_files = InputParser.parse_userinput("../../example/NoUserAnnotation.json")
#start_up, fuzz_internal_files, kitty_modals = InputParser.parse_userinput("../../example/UserAnnotated.json")
#Step 2: If any user annotated inputs are files, then back them up
#if backup_input_files is not None:
#    __binary_file = open(input_file_backup_data_binary, mode='w')
#    pickle.dump(backup_input_files, __binary_file)
#    __binary_file.close()
#exit(0) #ToDo: Only for testing. Remove.
#Step 3: If user has asked for fuzzing of internal file reads, back up the input files (because we will be modifying them)
#if backup_source_files is not None:
    #__generate_fuzz_file_for_fuzzinternalfilereads()
#    __binary_file = open(source_file_backup_data_binary, mode='w')
#    pickle.dump(backup_source_files, __binary_file)
#    __binary_file.close()
#Fuzzing input
for index, modal in enumerate(kitty_modals):
    __generate_fuzz_data(index, modal)
__experiment_generator_obj = ExperimentGenerator()
__experiment_generator_obj.set_startup_scripts(start_up)
__experiment_generator_obj.generate_experiment_json()