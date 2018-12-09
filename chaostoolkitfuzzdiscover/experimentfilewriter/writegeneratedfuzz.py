import glob
import json
import os
import sys
from chaostoolkitfuzzdiscover.constants.tmpfilenames import experiment_file_destination, fuzz_Input_data_location, chaostoolkit_fuzzdicover_root, tmp_folder, internal_read_mock_file

class ExperimentGenerator():

    def __init__(self):
        self.experiment_json_obj = {}
        self.experiment_methods = []
        self.experiment_steady_state_hypothesis = None
        self.experiment_rollbacks = []
        if not os.path.exists(experiment_file_destination):
            os.makedirs(experiment_file_destination)
        if "chaostoolitfuzzdiscover_steadystatehypothesis" not in sys.path:
            module_path = os.path.dirname(os.path.dirname(__file__))+"/chaostoolkitfuzzdiscover_steadystatehypothesis"
            sys.path.append(module_path)

    def __get_steady_state_hypothesis(self):
        __steady_state_hypothesis = {}
        __probes = []
        __consolidated_probe = {}
        __provider = {}
        __provider["type"] = "python"
        __provider["module"] = "chaostoolkitfuzzdiscover_checksteadystate"
        __provider["func"] = "check_probe"
        __consolidated_probe["tolerance"] = True
        __consolidated_probe["type"] = "probe"
        __consolidated_probe["provider"] = __provider
        __consolidated_probe["name"] = "fuzzdiscover-consolidated-systemic-issue-checking-probe"
        __steady_state_hypothesis["title"] = "Checking : Memory Leaks, Filesystem usage spikes, CPU utilization spikes, DB connection pool exhaustion, fork bombs"
        __steady_state_hypothesis["probes"] = [__consolidated_probe]
        return __steady_state_hypothesis

    def generate_experiment_json(self, __postfix):
        self.experiment_json_obj = {}
        self.experiment_json_obj["rollbacks"] = self.experiment_rollbacks
        self.experiment_json_obj["method"] = self.experiment_methods
        self.experiment_json_obj["steady-state-hypothesis"] = ExperimentGenerator.__get_steady_state_hypothesis(self)
        self.experiment_json_obj["tags"] = ["chaostoolkitfuzzdiscover-generated-experiment"]
        self.experiment_json_obj["description"] = "My FuzzDiscover Experiment"
        self.experiment_json_obj["title"] = "My FuzzDiscover Experiment"
        __experiment_file = open(experiment_file_destination+"experiment"+__postfix+".json", mode='w')
        json.dump(self.experiment_json_obj, __experiment_file, indent=4)

    def set_startup_scripts(self, start_up_scripts):
        __clean_up_action = {}
        __clean_up_action["type"] = "action"
        __clean_up_action["provider"] = {}
        __clean_up_action["name"] = "fuzz_discover_cleanup"
        __clean_up_action["provider"]["type"] = "process"
        __clean_up_action["provider"]["path"] = "rm"
        __clean_up_action["provider"]["arguments"] = "-r " + chaostoolkit_fuzzdicover_root
        self.experiment_rollbacks.insert(0, __clean_up_action)
        for __script in start_up_scripts:
            __sections = __script.split(" ", 1)
            __action = {}
            __action["type"] = "action"
            __action["provider"] = {}
            __action["name"] = "startup-script"
            __action["provider"]["type"] = "process"
            __action["provider"]["path"] = __sections[0]
            if len(__sections) > 0:
                __action["provider"]["arguments"] = __sections[1].rstrip("\n")
            else:
                __action["provider"]["arguments"] = " "
            self.experiment_rollbacks.insert(len(self.experiment_rollbacks), __action)

class InputFuzzExperimentGenerator(ExperimentGenerator):

    def __init__(self):
        ExperimentGenerator.__init__(self)
        self.fuzz_output_location = fuzz_Input_data_location
        os.system('chmod 755 ' + self.fuzz_output_location.rstrip("\n") + "*")
        files = glob.glob(self.fuzz_output_location.rstrip("\n") + "*")
        __permission_action = {}
        __permission_action["type"] = "action"
        __permission_action["provider"] = {}
        __permission_action["name"] = "setting-run-permissions"
        __permission_action["provider"]["type"] = "process"
        __permission_action["provider"]["path"] = "chmod"
        __permission_action["provider"]["arguments"] = "755 " + self.fuzz_output_location.rstrip("\n") + "*"
        self.experiment_methods.insert(len(self.experiment_methods), __permission_action)
        for name in files:
            __action = {}
            __action["type"] = "action"
            __action["provider"] = {}
            __action["name"] = "running-fuzzed-input"
            __action["provider"]["type"] = "process"
            __action["provider"]["path"] = name.rstrip("\n")
            __action["provider"]["arguments"] = "1"
            self.experiment_methods.insert(len(self.experiment_methods), __action)

class InputFileFuzzExperimentGenerator(ExperimentGenerator):

    def __init__(self, __input_files, __input_cmd):
        ExperimentGenerator.__init__(self)
        self.fuzz_output_location = tmp_folder
        if "chaostoolitfuzzdiscover_steadystatehypothesis" not in sys.path:
            module_path = os.path.dirname(os.path.dirname(__file__))+"/chaostoolkitfuzzdiscover_steadystatehypothesis"
            sys.path.append(module_path)
        files = glob.glob(self.fuzz_output_location.rstrip("\n") + "*")
        for name in files:
            for __backup in __input_files:
                __copy_action = {}
                __copy_action["type"] = "action"
                __copy_action["provider"] = {}
                __copy_action["name"] = "copy-fuzz-to-input-file"
                __copy_action["provider"]["type"] = "process"
                __copy_action["provider"]["path"] = "cp"
                __copy_action["provider"]["arguments"] = str(name) + " " + str(__backup["original"])
                self.experiment_methods.insert(len(self.experiment_methods), __copy_action)
            for __cmd in __input_cmd:
                __tokens = str(__cmd).split(" ", 1)
                __run_normal_input_action = {}
                __run_normal_input_action["type"] = "action"
                __run_normal_input_action["provider"] = {}
                __run_normal_input_action["name"] = "run-normal-execution"
                __run_normal_input_action["provider"]["type"] = "process"
                __run_normal_input_action["provider"]["path"] = str(__tokens[0])
                __run_normal_input_action["provider"]["arguments"] = str(__tokens[1]).rstrip("\n")
                self.experiment_methods.insert(len(self.experiment_methods), __run_normal_input_action)

    def set_startup_scripts(self, start_up_scripts):
        ExperimentGenerator.set_startup_scripts(self, start_up_scripts)
        __clean_up_action = {}
        __clean_up_action["type"] = "action"
        __clean_up_action["provider"] = {}
        __clean_up_action["name"] = "fuzz_discover_restore"
        __clean_up_action["provider"]["type"] = "process"
        __clean_up_action["provider"]["path"] = "python"
        __clean_up_action["provider"]["arguments"] = str(os.path.dirname(os.path.dirname(__file__)))+"/restoreinputfilebackup.py"
        self.experiment_rollbacks.insert(0, __clean_up_action)

class InternalFileFuzzExperimentGenerator(ExperimentGenerator):

    def __init__(self, __input_cmd):
        ExperimentGenerator.__init__(self)
        self.fuzz_output_location = tmp_folder
        files = glob.glob(self.fuzz_output_location.rstrip("\n") + "*")
        for name in files:
            __copy_action = {}
            __copy_action["type"] = "action"
            __copy_action["provider"] = {}
            __copy_action["name"] = "copy-fuzz-to-internal-file"
            __copy_action["provider"]["type"] = "process"
            __copy_action["provider"]["path"] = "cp"
            __copy_action["provider"]["arguments"] = str(name) + " " + internal_read_mock_file
            self.experiment_methods.insert(len(self.experiment_methods), __copy_action)
            for __cmd in __input_cmd:
                __tokens = str(__cmd).split(" ", 1)
                __run_normal_input_action = {}
                __run_normal_input_action["type"] = "action"
                __run_normal_input_action["provider"] = {}
                __run_normal_input_action["name"] = "run-normal-execution"
                __run_normal_input_action["provider"]["type"] = "process"
                __run_normal_input_action["provider"]["path"] = str(__tokens[0])
                __run_normal_input_action["provider"]["arguments"] = str(__tokens[1]).rstrip("\n")
                self.experiment_methods.insert(len(self.experiment_methods), __run_normal_input_action)

    def set_startup_scripts(self, start_up_scripts):
        ExperimentGenerator.set_startup_scripts(self, start_up_scripts)
        __clean_up_action = {}
        __clean_up_action["type"] = "action"
        __clean_up_action["provider"] = {}
        __clean_up_action["name"] = "fuzz_discover_restore"
        __clean_up_action["provider"]["type"] = "process"
        __clean_up_action["provider"]["path"] = "python"
        __clean_up_action["provider"]["arguments"] = str(os.path.dirname(os.path.dirname(__file__)))+"/restoresourcebackup.py"
        self.experiment_rollbacks.insert(0, __clean_up_action)

