from filenames import probe_file_destination, probe_start_indicator, final_top_cmd_dump, initial_top_cmd_dump, fuzz_Input_data_location, initial_df_cmd_dump, final_df_cmd_dump
import os
import shutil
import datetime
import time
#ToDo: Warning: tolerance for deviation in system state values is hardcoded and need to be refined
__number_of_top_vals_to_sample = 10

def check_probe():
    if os.path.exists(probe_start_indicator):
        time.sleep(10) #Adding 10 second sleep time for cooling off memory util overhead from experiment
        os.system("top -n 0 -l "+str(__number_of_top_vals_to_sample)+" > "+final_top_cmd_dump)
        os.system("df -m > "+final_df_cmd_dump)
        os.remove(probe_start_indicator)
        shutil.rmtree(fuzz_Input_data_location) #Clean-up has to occur here to account for filesystem util overhead from experiment itself
        __min_initial_cpu_idle, __min_initial_mem_unused, __max_initial_process_count, __min_final_cpu_idle, __min_final_mem_unused, __max_final_process_count = __parse_top_cmd_profiling_data()
        __avail_disk = __parse_df_cmd_profiling_data()
        return __check_cpu_util_tolerance(__min_initial_cpu_idle, __min_final_cpu_idle) and __check_mem_util_tolerance(__min_initial_mem_unused, __min_final_mem_unused) and __check_process_count_tolerance(__max_initial_process_count, __max_final_process_count) and __check_file_util_tolerance(__avail_disk)
    else:
        if os.path.exists(probe_file_destination):
            shutil.rmtree(probe_file_destination)
        if not os.path.exists(probe_file_destination):
            os.makedirs(probe_file_destination)
        __probe_indicator = open(probe_start_indicator, 'w')
        __probe_indicator.write("Probe_started_on: "+str(datetime.datetime.now()))
        __probe_indicator.close()
        os.system("top -n 0 -l "+str(__number_of_top_vals_to_sample)+" > " + initial_top_cmd_dump)
        os.system("df -m > "+initial_df_cmd_dump)
        return True

def __get_file_util_from_df_cmd(__file_name, __disk_util_dict, __key):
    with open(__file_name, 'r') as __ini_file:
        for __index, __line in enumerate(__ini_file):
            if __index is 0:
                continue
            __tokens = __line.split()
            __disk_name = __tokens[0]
            __available_disk_space_for_disk = __tokens[3]
            if __disk_name not in __disk_util_dict:
                __disk_util_dict[__disk_name] = {}
            __disk_util_dict[__disk_name][__key] = int(__available_disk_space_for_disk)
    return __disk_util_dict

def __parse_df_cmd_profiling_data():
    __disk_util_dict = {}
    __disk_util_dict = __get_file_util_from_df_cmd(initial_df_cmd_dump, __disk_util_dict, "initial")
    __disk_util_dict = __get_file_util_from_df_cmd(final_df_cmd_dump, __disk_util_dict, "final")
    return __disk_util_dict

def __check_file_util_tolerance(__disk_util_dict):
    __sum_initial = __sum_final = 0
    for __key in __disk_util_dict:
        if "initial" not in __disk_util_dict[__key] or "final" not in __disk_util_dict[__key]:
            continue #The disk was unmounted or mounted in the middle of the experiment. Ignore.
        __inital_val = __disk_util_dict[__key]["initial"]
        __final_val = __disk_util_dict[__key]["final"]
        print ("Filesystem space available in MB in disk "+str(__key)+" Initial: " + str(__inital_val) + " Final: " + str(__final_val))
        __sum_initial+=__inital_val
        __sum_final+=__final_val
        if __inital_val - __final_val > 50: #ToDO: Warning: Hardcoded tolerance to delta of 50 MB
            print ("chaostoolkitfuzzdiscover][ERROR]:  Filesystem space available in MB in disk " + str(__key) + " decreased abnormally. Initial: " + str(__inital_val) + " Final: " + str(__final_val))
            return False
        if __inital_val - __final_val > 50: #ToDO: Warning: Hardcoded tolerance to delta of 50 MB
            print ("chaostoolkitfuzzdiscover][ERROR]:  Total Filesystem space available in MB in disk " + str(__key) + " decreased abnormally. Initial: " + str(__sum_initial) + " Final: " + str(__sum_final))
            return False
    return True

def __check_cpu_util_tolerance(__initial_val, __final_val):
    if __final_val < 2.0 or __final_val < __initial_val/2: #ToDO: Warning: Hardcoded tolerance
        print ("chaostoolkitfuzzdiscover][ERROR]: CPU utilization exceeded abnormally since the start of the experiment. Inital idle time val: "+str(__initial_val)+" Final idle time val: "+str(__final_val))
        return False
    print ("CPU Idle time. Initial: "+str(__initial_val)+" Final: "+str(__final_val))
    return True

def __check_mem_util_tolerance(__initial_val, __final_val):
    if __final_val < __initial_val*0.5: #ToDO: Warning: Hardcoded tolerance
        print ("[chaostoolkitfuzzdiscover][ERROR]: Memory utilization exceeded abnormally since the start of the experiment Inital unused val: "+str(__initial_val)+" Final unused val: "+str(__final_val))
        return False
    print ("Memory unused. Initial: " + str(__initial_val) + " Final: " + str(__final_val))
    return True

def __check_process_count_tolerance(__inital_val, __final_val):
    if __final_val >= 1.5 * __inital_val: #ToDO: Warning: Hardcoded tolerance
        print ("chaostoolkitfuzzdiscover][ERROR]: Process count exceeded abnormally since the start of the experiment Inital val: "+str(__inital_val)+" Final val: "+str(__final_val))
        return False
    print ("Process count. Initial: " + str(__inital_val) + " Final: " + str(__final_val))
    return True

def __get_system_state_from_top_cmd(__file_name):
    __initial_cpu_idle = 100.0
    __min_initial_mem_unused = 99999999
    __max_initial_process_count = 0
    with open(__file_name, 'r') as __inital_file:
        for __line in __inital_file:
            if "Processes:" in __line:
                __tokens = __line.split(" ")
                __process_count = __tokens[1]
                __max_initial_process_count = max(__max_initial_process_count, int(__process_count))
            if "CPU usage:" in __line:
                __tokens = __line.split(" ")
                __cpu_idle_time = __tokens[-3]
                __cpu_idle_time = __cpu_idle_time.rstrip("%")
                __initial_cpu_idle += float(__cpu_idle_time)
            if "PhysMem:" in __line:
                __tokens = __line.split(" ")
                __mem_unused = __tokens[-2]
                __mem_unused = __mem_unused.rstrip("M")
                __min_initial_mem_unused = min(__min_initial_mem_unused, int(__mem_unused))
    __initial_cpu_idle = __initial_cpu_idle / __number_of_top_vals_to_sample
    return __initial_cpu_idle, __min_initial_mem_unused, __max_initial_process_count

def __parse_top_cmd_profiling_data():
    __min_initial_cpu_idle, __min_initial_mem_unused, __max_initial_process_count = __get_system_state_from_top_cmd(initial_top_cmd_dump)
    __min_final_cpu_idle, __min_final_mem_unused, __max_final_process_count = __get_system_state_from_top_cmd(final_top_cmd_dump)
    return __min_initial_cpu_idle, __min_initial_mem_unused, __max_initial_process_count, __min_final_cpu_idle, __min_final_mem_unused, __max_final_process_count