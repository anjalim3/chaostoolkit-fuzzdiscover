import json
from kitty.model import *
from unannotatedinputparser import UnannotatedInputParser
from annotatedinputparser import AnnotatedInputParser
from chaostoolkitfuzzdiscover.fuzzinternalfilereads.instrumentsource import instrument_source

#ToDo Add input validation
class InputParser:

    @staticmethod
    def parse_userinput(input_file_url):
        with open(input_file_url, 'r') as inputfile:
            data = inputfile.read().replace('\n', ' ')
        python_obj = json.loads(data)
        sample_input = python_obj["sample_input"]
        start_up = python_obj["start_up"]
        if "fuzz_internal_files_path_to_sources" in python_obj:
            fuzz_internal_files = python_obj["fuzz_internal_files_path_to_sources"]
        else:
            fuzz_internal_files = None
        if "is_annotated" in python_obj:
            is_annotated = True if python_obj["is_annotated"] == "true" else False
        else:
            is_annotated = False
        modals = [InputParser.__get_kitty_models_from_sample_input(sample_input, is_annotated)]
        if fuzz_internal_files is not None:
            instrument_source(fuzz_internal_files)
        return start_up, fuzz_internal_files, modals

    @staticmethod
    def __get_kitty_models_from_sample_input(sample_input, is_annotated):
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
