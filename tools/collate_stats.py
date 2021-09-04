import os
import sys
import json

script_path = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else f"{script_path}/../output"
result_outputs = ["t1_final", "t2_final", "t3_final", "t4_final"]

collated = dict()

for task_num,output in enumerate(result_outputs, start=1):
    logpath = output_path+"/"+output
    logfile = logpath+"/log.txt"
    outputfile = logpath+"/stats.json"
    print(f"Processing logfile: {logfile} -> {outputfile}")
    os.system(f"python {script_path}/extract_stats.py < {logfile} > {outputfile}")
    with open(outputfile, 'r') as statsfd:
        stats = json.load(statsfd)
        collated[f"Task {task_num}"]=stats

train_outputs = ["t1", "t2", "t2_ft", "t3", "t3_ft", "t4", "t4_ft"]

for task_num in range(1, 5):
    for fine_tune in [False, True]:
        if task_num == 1 and fine_tune:
            continue
        suffix = fine_tune and "_ft" or ""
        output = f"t{task_num}{suffix}"
        logpath = output_path+"/"+output
        logfile = logpath+"/log.txt"
        outputfile = logpath+"/timings.json"
        print(f"Processing logfile: {logfile} -> {outputfile}")
        os.system(f"python {script_path}/extract_timings.py < {logfile} > {outputfile}")
        stat_key = fine_tune and "Fine Tune" or "Train"
        with open(outputfile, 'r') as statsfd:
            stats = json.load(statsfd)
            if "Timings" not in collated[f"Task {task_num}"]:
                collated[f"Task {task_num}"]["Timings"] = dict()
            collated[f"Task {task_num}"]["Timings"][stat_key]=stats


final_stats_path = f"{output_path}/stats.json"
print(f"Outputting collated data to {final_stats_path}")
with open(final_stats_path, "w") as statsfd:
    json.dump(collated, statsfd, indent=4)
