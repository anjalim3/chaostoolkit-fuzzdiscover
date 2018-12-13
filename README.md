# chaostoolkit-fuzzdiscover
Fuzz test experiment suggester for ChaosToolkit

Gives "suggestions" for chaostoolkit experiments to run.

The experiments only aims to check for system health, i.e, the experiments do not care if a particular call fails due to bad input.
The experiments are concerned with finding and surfacing cases when bad inputs will irrecoverably detriment system's health,
such as causing the service itself to fatally crash and never recover, dump files and never cleanup, cause persisting stress on CPU and Memory Utilization etc.

Find more under examples and demo_run.py

## Setup

Requires kittyfuzzer, katnip for setup

For setting up ChaosToolkit: https://docs.chaostoolkit.org/reference/usage/install/


## Input Structure
### start_up :
 Script(s) to run to reset the environment and application. Will not be fuzzed.
Can be omitted.

### sample_input : 
Input(s) for the application. Will be fuzzed.
sample_input can be annotated or unannotated.

#### Annotated:
If annotated, then only the blocks or parts of input specified by user will be fuzzed.
Currently supported annotations are Number and String

#### UnAnnotated:
If not annotated, then our tool tries to figure out structure of input on its own.

### fuzz_internal_files : 
Tells tool if it should fuzz all files read by the application.
Works by instrumenting the source code, i.e. replaces calls for any file read with file read for fuzzed file - literally does `sed`
The source code will be "uninstrumented" to original version after test.
Currently supports only python
#### Disclaimer: Might not replace all file reads
#### ToDo: Add support for other languages. For the duration for which "modified" code is in use, all service calls will fail. Need a fix to minimize application down time.

## Sample Input

### UnAnnotated Input

    {
      "start_up" :
      ["python3 ~/chaos_demo/chaostoolkit-documentation-code/tutorials/a-simple-walkthrough/sunset.py",
        "python3 ~/chaos_demo/chaostoolkit-documentation-code/tutorials/a-simple-walkthrough/sunset.py"],
    
      "sample_input" : ["curl -k https://localhost:84.43/city/Chicago","curl -k https://localhost:84.43/city/Paris"],
    
      "fuzz_internal_files" : ["~/chaos_demo/chaostoolkit-documentation-code/tutorials/a-simple-walkthrough/sunset.py",
    "~/chaos_demo/chaostoolkit-documentation-code/tutorials/a-simple-walkthrough/sunset.py"]
    }

#Steady State Hypothesis
Before beginning the experiment we profile system state for 10s and collect the data.
After finishing the experiment, we profile the system state once more for 10s and check if there are any major discrepancies from the first collected data.

#ToDo
Add more annotation support. Required annotations: File, Enum
Improve the intelligence of "figuring out"
