# Nth Fibonacci Number Demo

This is the demo for generating nth Fibonacci number.

### What our demo Fibo generator does:
The program accepts multiple values for "n" and generates the corresponding nth Fibonacci number in each case.

### Internals of the Fibo generator:
It accepts multiple values for "n" as commandline input and stores them in a file.
It later reads the file line by line and finds the nth Fibonnaci number for each of the values of n.


### What bug are we uncovering:
"Segmentation failures" and memory exhaustions in general make systems "core dump" a consolidated byte-code file for debugging purposes.
These "core dumps" (hprofs in case of JVM) are large files - running from few hundred MBs to few GBs in size - that eat up file system space.

Core dumps usually slowly eat up disk space with each failure till one day you suddenly wake up to a full disk _[Real production issue]_


### What FuzzDiscover does in this demo:
FuzzDiscover replaces all the internal file reads in our source code to read the fuzzed file "fuzzed.txt" instead of whatever file it was actually meant to read.

Therefore, when the experiments are run, the file that willl be read for generating nth Fibo number will be our fuzzed file.

Some of our fuzz values are abnormally large which will cause our demo program to go into a deep recursion. 
This deep recursion will cause a resource(memory) exhaustion and force the python interpretter to crash with "segmentation failure". 

After the experiment is complete fuzzdiscover and chaostoolkit do a rollback to restore the original source files.

### Setup

1. Make a copy this folder 'fibo_demo' with all its contents into /tmp. Do not remove the original folder from this location.
2. Check if your system allows core dump by executing:
    `ulimit -c`
3. If step #2 returned 0 or any value other than "unlimited" , allow system to core dump by running:
    `ulimit -c unlimited`

**If you are running the experiment from inside a python virtual environment or any container, then `ulimit` needs to be set there.**

You can set you core dump limit back after finishing demo by running:
    `ulimit -c <initial_value_from_step_2_above>`

### Running the demo

1. Generate the experiment json file by running the corresponding demo in run/demo_run.py. 
    This generates the file "experiment_internal_file_read_fuzz_only.json" in "/tmp/chaostoolkitfuzzdiscover/experiment"
    
2. Run the command below

   `chaos run /tmp/chaostoolkitfuzzdiscover/experiment/experiment_internal_file_read_fuzz_only.json`
