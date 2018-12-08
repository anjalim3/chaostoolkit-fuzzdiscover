from filenames import probe_file_destination, probe_start_indicator, final_top_cmd_dump, initial_top_cmd_dump
import os
import shutil
import datetime
import time
#ToDo: Warning: tolerance for deviation in system state values is hardcoded and need to be refined

def check_probe():
    if os.path.exists(probe_start_indicator):
        time.sleep(10) #Adding 10 second sleep time for cooling off cpu or memory overhead from experiment
        os.system("top -n 0 -l 10 > "+final_top_cmd_dump)
        os.remove(probe_start_indicator)
        __min_initial_cpu_idle, __min_initial_mem_unused, __max_initial_process_count, __min_final_cpu_idle, __min_final_mem_unused, __max_final_process_count = __parse_top_cmd_profiling_data()
        return __check_cpu_util_tolerance(__min_initial_cpu_idle, __min_final_cpu_idle) and __check_mem_util_tolerance(__min_initial_mem_unused, __min_final_mem_unused) and __check_process_count_tolerance(__max_initial_process_count, __max_final_process_count)
    else:
        if os.path.exists(probe_file_destination):
            shutil.rmtree(probe_file_destination)
        if not os.path.exists(probe_file_destination):
            os.makedirs(probe_file_destination)
        __probe_indicator = open(probe_start_indicator, 'w')
        __probe_indicator.write("Probe_started_on: "+str(datetime.datetime.now()))
        __probe_indicator.close()
        os.system("top -n 0 -l 10 > " + initial_top_cmd_dump)
        return True

def __check_cpu_util_tolerance(__initial_val, __final_val):
    if __final_val < 2.0 or __final_val < __initial_val/2: #ToDO: Warning: Hardcoded tolerance
        print ("CPU utilization exceeded abnormally since the start of the experiment. Inital val: "+str(__initial_val)+" Final val: "+str(__final_val))
        return False
    return True

def __check_mem_util_tolerance(__initial_val, __final_val):
    if __final_val < 1000 or __final_val < __initial_val*0.9: #ToDO: Warning: Hardcoded tolerance
        print ("Memory utilization exceeded abnormally since the start of the experiment Inital val: "+str(__initial_val)+" Final val: "+str(__final_val))
        return False
    return True

def __check_process_count_tolerance(__inital_val, __final_val):
    if __final_val >= 1.5 * __inital_val: #ToDO: Warning: Hardcoded tolerance
        print ("Process count exceeded abnormally since the start of the experiment Inital val: "+str(__inital_val)+" Final val: "+str(__final_val))
        return False
    return True

def __get_system_state_from_top_cmd(__file_name):
    __min_initial_cpu_idle = 0.0
    __min_initial_mem_unused = 0
    __max_initial_process_count = 0
    with open(initial_top_cmd_dump, 'r') as __inital_file:
        __line = __inital_file.readline()
        if "Processes:" in __line:
            __tokens = __line.split(" ")
            __process_count = __tokens[1]
            __max_initial_process_count = max(__max_initial_process_count, int(__process_count))
        if "CPU usage:" in __line:
            __tokens = __line.split(" ")
            __cpu_idle_time = __tokens[-2]
            __cpu_idle_time = __cpu_idle_time.rstrip("%")
            __min_initial_cpu_idle = min(__min_initial_cpu_idle, float(__cpu_idle_time))
        if "PhysMem:" in __line:
            __tokens = __line.split(" ")
            __mem_unused = __tokens[-2]
            __min_initial_mem_unused = min(__min_initial_mem_unused, int(__mem_unused))
    return __min_initial_cpu_idle, __min_initial_mem_unused, __max_initial_process_count

def __parse_top_cmd_profiling_data():
    __min_initial_cpu_idle = 0.0
    __min_initial_mem_unused = 0
    __max_initial_process_count = 0
    __min_initial_cpu_idle, __min_initial_mem_unused, __max_initial_process_count = __get_system_state_from_top_cmd(initial_top_cmd_dump)
    __min_final_cpu_idle = 0.0
    __min_final_mem_unused = 0
    __max_final_process_count = 0
    __min_final_cpu_idle, __min_final_mem_unused, __max_final_process_count = __get_system_state_from_top_cmd(final_top_cmd_dump)
    return __min_initial_cpu_idle, __min_initial_mem_unused, __max_initial_process_count, __min_final_cpu_idle, __min_final_mem_unused, __max_final_process_count


