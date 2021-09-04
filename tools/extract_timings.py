# %% test
import sys
import re
import json


def new_stats():
    return {
        "GPU": None,
        "Task": None,
        "Iters" : None,
        "Scaled_Iters": None,
        "Seconds_Per_Iter": None,
        "Duration_Seconds": None
    }

stats = new_stats()
# %% test
gpu_re = re.compile("^GPU \\d\\s+(?P<value>.*)$")
task_re = re.compile(".*Contents of args.config_file=.*/t\\d/(?P<value>.*)\\.yaml")
iter_re = re.compile("\\s+MAX_ITER: (?P<value>\\d+)")
scaled_iters_re = re.compile(".*INFO: Auto-scaling the config to .* max_iter=(?P<value>\\d+),")
time_re = re.compile(".*INFO: Overall training speed: .* iterations in (?:(?P<days>\\d+) da.*, )?(?P<hours>\\d+):(?P<mins>\\d+):(?P<sec>\\d+) \\((?P<periter>[\\d\\.]+) s / it\\)")

reset_re = gpu_re


# %% 
for line in sys.stdin:

    m = reset_re.match(line)
    if m:
        stats = new_stats()

    m = gpu_re.match(line)
    if m:
        stats["GPU"] = m.groupdict()["value"]
        continue

    m = task_re.match(line)
    if m:
        stats["Task"] = m.groupdict()["value"]
        continue
  
    m = iter_re.match(line)
    if m:
        stats["Iters"] = float(m.groupdict()["value"])
        continue

    m = scaled_iters_re.match(line)
    if m:
        stats["Scaled_Iters"] = float(m.groupdict()["value"])
        continue

    m = time_re.match(line)
    if m:
        stats["Seconds_Per_Iter"] = float(m.groupdict()["periter"])
        
        days = float(m.groupdict()["days"] or 0)
        hours = float(m.groupdict()["hours"])
        mins = float(m.groupdict()["mins"])
        sec = float(m.groupdict()["sec"])
        stats["Duration_Seconds"] = ((days * 24 + hours) * 60 + mins) * 60 + sec
        continue

print(json.dumps(stats, indent=4))


