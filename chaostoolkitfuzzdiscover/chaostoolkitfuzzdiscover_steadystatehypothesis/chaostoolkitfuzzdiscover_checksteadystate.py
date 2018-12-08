from filenames import probe_file_destination, probe_start_indicator, final_top_cmd_dump, initial_top_cmd_dump
import os
import shutil
import datetime

def check_probe():
    if os.path.exists(probe_start_indicator):
        os.system("top -n 0 -l 10 > "+final_top_cmd_dump)
        os.remove(probe_start_indicator)
        return False
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

def hello():
    dir_path = os.path.dirname(os.path.dirname(__file__))
    print (dir_path)
    return True
