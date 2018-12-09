import chaostoolkitfuzzdiscover.run.start
from chaostoolkitfuzzdiscover_steadystatehypothesis.filenames import chaostoolkit_fuzzdicover_root
import os
import shutil

__example_root_folder = os.path.dirname(os.path.dirname(__file__))
__unAnnotated_Example = __example_root_folder+"/example/NoUserAnnotation.json"
__annotated_Example = __example_root_folder+"/example/UserAnnotated.json"

#Clean_up just in case
if os.path.exists(chaostoolkit_fuzzdicover_root):
    shutil.rmtree(chaostoolkit_fuzzdicover_root)


"""
Sample demo runs below. 

RUN one at a time and comment out the rest.

#1 : HappyCase: UnAnnotated User Input Fuzzing

"""



""" Demo 1: User Input Fuzzing HappyCase """
#chaostoolkitfuzzdiscover.run.start.chaostoolkit_fuzzexperiment_wInputFuzzing(__unAnnotated_Example)


""" Demo 2: User Input File Fuzzing """
#chaostoolkitfuzzdiscover.run.start.chaostoolkit_fuzzexperiment_Input_File_Fuzzing(__unAnnotated_Example)


""" Demo 3: Internal Input File Fuzzing """
chaostoolkitfuzzdiscover.run.start.chaostoolkit_fuzzexperiment_Internal_File_Read_Fuzzing(__unAnnotated_Example)