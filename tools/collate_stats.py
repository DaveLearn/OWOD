import os
import sys
import json

script_path = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else f"{script_path}/../output"
result_outputs = ["t1", "t1_final", "t2", "t2_ft", "t2_final", "t3", "t3_ft", "t3_final", "t4", "t4_ft", "t4_final"]

experiment_folder = os.path.basename(os.path.normpath(output_path))
collated = dict()
collated['Experiment_Folder'] = experiment_folder

for task_num,output in enumerate(result_outputs, start=1):
    
    logpath = output_path+"/"+output
    logfile = logpath+"/log.txt"
    outputfile = logpath+"/stats.json"
    timingfile = logpath+"/timings.json"
    print(f"Processing logfile: {logfile} -> {outputfile}")
    if not os.path.exists(logfile):
        print(f"  File not found - skipping")
        continue

    os.system(f"python {script_path}/extract_stats.py < {logfile} > {outputfile}")
    os.system(f"python {script_path}/extract_timings.py < {logfile} > {timingfile}")
    with open(timingfile, 'r') as statsfd:
        timings = json.load(statsfd)

    with open(outputfile, 'r') as statsfd:
        stats = json.load(statsfd)
        stats["Timings"] = timings
        task_name = output[1:].replace('_', ' ').replace('f', 'F')
        collated[f"Task {task_name}"]=stats


final_stats_path = f"{output_path}/stats.json"
print(f"Outputting collated data to {final_stats_path}")
with open(final_stats_path, "w") as statsfd:
    json.dump(collated, statsfd, indent=4)
