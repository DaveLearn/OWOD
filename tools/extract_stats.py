import sys
import re
import json

def precision_recall_ap50():
    return {
        "Precisions50": None,
        "Recall50": None,
        "AP50": None
    }


def new_stats():
    return {
        "T1 class": precision_recall_ap50(),
        "T2 class": precision_recall_ap50(),
        "T3 class": precision_recall_ap50(),
        "T4 class": precision_recall_ap50(),
        "Prev class": precision_recall_ap50(),
        "Current class": precision_recall_ap50(),
        "Known": precision_recall_ap50(),
        "Unknown": precision_recall_ap50(),
        "Absolute OSE": None,
        "Wilderness Impact": None
    }

stats = new_stats()

prec_full_re = re.compile(".*INFO: (?P<stat>(AP50|Precisions50|Recall50)): (?P<data>\\[.*\\])")

prec_re = re.compile(".*INFO: (?P<classes>(Current class|Prev class|Known|Unknown)) (?P<stat>(AP50|Precisions50|Recall50)): (?P<value>[\\d\\.]+)$")
ose_re = re.compile(".*INFO: Absolute OSE \\(total_num_unk_det_as_known\\): \\{50: (?P<value>[\\d\\.]+)\\}")
wi_re = re.compile(".*INFO: Wilderness Impact: \\{.*, 0\\.8: \\{50: (?P<value>[\\d\\.]+)\\}")
reset_re = re.compile(".*Evaluating voc_coco_2007_test using 2012 metric")
weights_re = re.compile(".*WEIGHTS: (?P<weights>.*\\.pth)")

evaluated_weights = None

for line in sys.stdin:
    m = weights_re.match(line)
    if m:
        evaluated_weights = m.groupdict()["weights"]

    m = reset_re.match(line)
    if m:
        stats = new_stats()

    m = prec_re.match(line)
    if m:
        d = m.groupdict()
        stats[d["classes"]][d["stat"]] = float(d["value"])
        continue

    m = prec_full_re.match(line)
    if m:
        d = m.groupdict()
        stat = d["stat"]
        values = [float(n) for n in json.loads(d["data"].replace("'", '"'))][:80]
        stats["T1 class"][stat] = round(sum(values[0:20])/20, 2)
        stats["T2 class"][stat] = round(sum(values[20:40])/20,2)
        stats["T3 class"][stat] = round(sum(values[40:60])/20,2)
        stats["T4 class"][stat] = round(sum(values[60:80])/20,2)

    m = ose_re.match(line)
    if m:
        stats["Absolute OSE"] = float(m.groupdict()["value"])
        continue

    m = wi_re.match(line)
    if m:
        stats["Wilderness Impact"] = float(m.groupdict()["value"])
        continue

stats["Weights"] = evaluated_weights

print(json.dumps(stats, indent=4))

    
