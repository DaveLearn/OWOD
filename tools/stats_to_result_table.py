import os
import sys
import json

script_path = os.path.dirname(os.path.abspath(__file__))

stats_path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else f"{script_path}/../output/stats.json"

sep = "|"
headers = ["T1-WI","T1-A-OSE", "T1-Current", 
           "T2-WI", "T2-A-OSE", "T2-Previous", 
           "T2-Current", "T2-Both", "T3-WI", 
           "T3-A-OSE", "T3-Previous", "T3-Current",
            "T3-Both", "T4-Previous", "T4-Current", "T4-Both"]

with (open(stats_path, "r")) as statsfd:
    stats = json.load(statsfd)
    #headers

    print(sep.join(headers))
    print("|".join(['-' for i in headers]))

    #row
    values = [
        format(stats['Task 1']["Wilderness Impact"], ".5f"),
        format(stats['Task 1']["Absolute OSE"], ".0f"),
        format(stats['Task 1']["Current class"]["AP50"], ".2f"),

        format(stats['Task 2']["Wilderness Impact"], ".5f"),
        format(stats['Task 2']["Absolute OSE"], ".0f"),
        format(stats['Task 2']["Prev class"]["AP50"], ".2f"),
        format(stats['Task 2']["Current class"]["AP50"], ".2f"),   
        format(stats['Task 2']["Known"]["AP50"], ".2f"),  

        format(stats['Task 3']["Wilderness Impact"], ".5f"),
        format(stats['Task 3']["Absolute OSE"], ".0f"),
        format(stats['Task 3']["Prev class"]["AP50"], ".2f"),
        format(stats['Task 3']["Current class"]["AP50"], ".2f"),   
        format(stats['Task 3']["Known"]["AP50"], ".2f"),   

        format(stats['Task 4']["Prev class"]["AP50"], ".2f"),
        format(stats['Task 4']["Current class"]["AP50"], ".2f"),   
        format(stats['Task 4']["Known"]["AP50"], ".2f")
    ]

    print(sep.join(values))