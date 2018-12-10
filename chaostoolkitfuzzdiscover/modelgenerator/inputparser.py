import json
from kitty.model import *
from unannotatedinputparser import UnannotatedInputParser
from annotatedinputparser import AnnotatedInputParser
from chaostoolkitfuzzdiscover.fuzzfilereads.instrumentsource import instrument_source

#ToDo Add input validation
class InputParser:

    @staticmethod
    def parse_userinput(input_file_url, suppress_input_fuzzing=False, suppress_input_file_fuzzing=False, suppress_internal_file_fuzzing=False):
        with open(input_file_url, 'r') as inputfile:
            data = inputfile.read().replace('\n', ' ')
        python_obj = json.loads(data)
        sample_input = python_obj["sample_input"]
        start_up = python_obj["start_up"]
        __backup_source_files = None
        __backup_input_files = None
        if not suppress_internal_file_fuzzing and "fuzz_internal_files_path_to_sources" in python_obj:
            fuzz_internal_files = python_obj["fuzz_internal_files_path_to_sources"]
        else:
            fuzz_internal_files = None
        if not suppress_input_file_fuzzing and "input_files" in python_obj:
            input_files = python_obj["input_files"]
        else:
            input_files = None
        if "is_annotated" in python_obj:
            is_annotated = True if python_obj["is_annotated"] == "true" else False
        else:
            is_annotated = False
        if not suppress_input_fuzzing:
            modals = [InputParser.get_kitty_models_from_sample_input(sample_input, is_annotated)]
        else:
            modals = None
        if fuzz_internal_files is not None:
            __backup_source_files = instrument_source(fuzz_internal_files, True)
        if input_files is not None:
            __backup_input_files = instrument_source(input_files, False)
        return start_up, fuzz_internal_files, modals, __backup_source_files, __backup_input_files, sample_input

    @staticmethod
    def get_kitty_models_from_sample_input(sample_input, is_annotated):
        templates = []
        for input_line in sample_input:
            if is_annotated:
                templates.append(AnnotatedInputParser.get_kittytemplate_from_input(input_line))
            else:
                templates.append(UnannotatedInputParser.get_kittytemplate_from_input(input_line))
        model = GraphModel()
        prev_template = None
        for index, template in enumerate(templates):
            if index == 0:
                model.connect(template)
            else:
                model.connect(prev_template, template)
            prev_template = template
        return None if len(templates) == 0 else model
