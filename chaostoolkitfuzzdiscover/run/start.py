from chaostoolkitfuzzdiscover.modelgenerator.inputparser import InputParser
from kitty.controllers import EmptyController
from kitty.fuzzers import ServerFuzzer
from kitty.interfaces import WebInterface
from katnip.targets.file import FileTarget

#TODO : Add input validations & fix input

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

start_up, fuzz_internal_files, kitty_modals = InputParser.parse_userinput("../../example/NoUserAnnotation.json")
#start_up, fuzz_internal_files, kitty_modals = InputParser.parse_userinput("../../example/UserAnnotated.json")
exit(0) #ToDo: Only for testing
for index, modal in enumerate(kitty_modals):
    __generate_fuzz_data(index, modal)