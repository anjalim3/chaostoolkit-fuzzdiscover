# chaostoolkit-fuzzdiscover
Fuzz test experiment suggester for ChaosToolkit

##Input Structure
start_up : script(s) to run to set up the environment. Will not be fuzzed.
Can be omitted

sample_input : input(s) for the application. Will be fuzzed.

fuzz_internal_files : should all files read by the application be fuzzed

## Sample Input

### UnAnnotated Input
::

    {
      "start_up" :
      ["python3 ~/chaos_demo/chaostoolkit-documentation-code/tutorials/a-simple-walkthrough/sunset.py",
        "python3 ~/chaos_demo/chaostoolkit-documentation-code/tutorials/a-simple-walkthrough/sunset.py"],
    
      "sample_input" : ["curl -k https://localhost:84.43/city/Chicago","curl -k https://localhost:84.43/city/Paris"],
    
      "fuzz_internal_files" : ["~/chaos_demo/chaostoolkit-documentation-code/tutorials/a-simple-walkthrough/sunset.py",
    "~/chaos_demo/chaostoolkit-documentation-code/tutorials/a-simple-walkthrough/sunset.py"]
    }

#ToDo
multiple input
annotated input