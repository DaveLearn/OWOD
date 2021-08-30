import os
import sys
import json

script_path = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else f"{script_path}/../output"
outputs = ["t1_final", "t2_final", "t3_final", "t4_final"]

collated = dict()

for task_num,output in enumerate(outputs, start=1):
    logpath = output_path+"/"+output
    logfile = logpath+"/log.txt"
    outputfile = logpath+"/stats.json"
    print(f"Processing logfile: {logfile} -> {outputfile}")
    os.system(f"python {script_path}/extract_stats.py < {logfile} > {outputfile}")
    with open(outputfile, 'r') as statsfd:
        stats = json.load(statsfd)
        collated[f"Task {task_num}"]=stats

final_stats_path = f"{output_path}/stats.json"
print(f"Outputting collated data to {final_stats_path}")
with open(final_stats_path, "w") as statsfd:
    json.dump(collated, statsfd, indent=4)

