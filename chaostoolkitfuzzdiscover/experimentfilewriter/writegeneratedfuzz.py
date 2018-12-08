import glob
import json
import os
import shutil
import sys
from chaostoolkitfuzzdiscover.constants.tmpfilenames import experiment_file_destination, fuzz_Input_data_location

class ExperimentGenerator:

    __fuzz_output_location = None
    __experiment_json_obj = {}
    __experiment_methods = []
    __experiment_steady_state_hypothesis = None
    __experiment_rollbacks = []

    def __init__(self):
        if os.path.exists(experiment_file_destination):
            shutil.rmtree(experiment_file_destination)
        if not os.path.exists(experiment_file_destination):
            os.makedirs(experiment_file_destination)
        self.__fuzz_output_location = fuzz_Input_data_location
        os.system('chmod 755 ' + self.__fuzz_output_location.rstrip("\n")+"*")
        if "chaostoolitfuzzdiscover_steadystatehypothesis" not in sys.path:
            module_path = os.path.dirname(os.path.dirname(__file__))+"/chaostoolkitfuzzdiscover_steadystatehypothesis"
            sys.path.append(module_path)
        files = glob.glob(self.__fuzz_output_location.rstrip("\n")+"*")
        __permission_action = {}
        __permission_action["type"] = "action"
        __permission_action["provider"] = {}
        __permission_action["name"] = "setting-run-permissions"
        __permission_action["provider"]["type"] = "process"
        __permission_action["provider"]["path"] = "chmod"
        __permission_action["provider"]["arguments"] = "755 " + self.__fuzz_output_location.rstrip("\n")+"*"
        self.__experiment_methods.insert(len(self.__experiment_methods), __permission_action)
        for name in files:
            __action = {}
            __action["type"] = "action"
            __action["provider"] = {}
            __action["name"] = "running-fuzzed-input"
            __action["provider"]["type"] = "process"
            __action["provider"]["path"] = name.rstrip("\n")
            __action["provider"]["arguments"] = "1"
            self.__experiment_methods.insert(len(self.__experiment_methods), __action)

    def generate_experiment_json(self):
        self.__experiment_json_obj = {}
        self.__experiment_json_obj["rollbacks"] = self.__experiment_rollbacks
        self.__experiment_json_obj["method"] = self.__experiment_methods
        self.__experiment_json_obj["steady-state-hypothesis"] = self.__get_steady_state_hypothesis()
        self.__experiment_json_obj["tags"] = ["chaostoolkitfuzzdiscover-generated-experiment"]
        self.__experiment_json_obj["description"] = "My FuzzDiscover Experiment"
        self.__experiment_json_obj["title"] = "My FuzzDiscover Experiment"
        __experiment_file = open(experiment_file_destination+"experiment.json", mode='w')
        json.dump(self.__experiment_json_obj, __experiment_file, indent=4)

    def set_startup_scripts(self, start_up_scripts):
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
                __action["provider"]["arguments"] = ""
            self.__experiment_rollbacks.insert(-1, __action)

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


