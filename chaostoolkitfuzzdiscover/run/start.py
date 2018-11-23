from chaostoolkitfuzzdiscover.modelgenerator.inputparser import InputParser
from chaostoolkitfuzzdiscover.fuzzinternalfilereads.instrumentsource import fuzzed_file_name
from chaostoolkitfuzzdiscover.constants.tmpfilenames import backup_data_binary
from kitty.controllers import EmptyController
from kitty.fuzzers import ServerFuzzer
from kitty.interfaces import WebInterface
from katnip.targets.file import FileTarget
from kitty.model import String
from kitty.model import Template
from kitty.model import GraphModel
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
    __tmp_folder = '../../tmp/'
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
    target = FileTarget('FileTarget', '../../output/', 'fuzzed'+str(index))
    target.set_controller(controller)
    fuzzer = ServerFuzzer()
    fuzzer.set_interface(WebInterface(port=26001))
    fuzzer.set_model(kitty_modal)
    fuzzer.set_target(target)
    fuzzer.start()
    fuzzer.stop()

start_up, fuzz_internal_files, kitty_modals, backup_files = InputParser.parse_userinput("../../example/NoUserAnnotation.json")
#start_up, fuzz_internal_files, kitty_modals = InputParser.parse_userinput("../../example/UserAnnotated.json")
if backup_files is not None:
    #__generate_fuzz_file_for_fuzzinternalfilereads()
    __binary_file = open(backup_data_binary, mode='w')
    pickle.dump(backup_files, __binary_file)
    __binary_file.close()
exit(0) #ToDo: Only for testing. Remove.
for index, modal in enumerate(kitty_modals):
    __generate_fuzz_data(index, modal)