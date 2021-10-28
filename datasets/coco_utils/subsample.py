import os
import random
dset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../VOC2007/ImageSets/Main'))
input_file = os.path.join(dset_path, 't4_ft_300.txt')
output_file = os.path.join(dset_path, 't4_ft_100.txt')

with open(input_file, "r") as inf:
    input_items = inf.readlines()

random.shuffle(input_items)

with open(output_file, "w+") as outf:
    outf.writelines(input_items[:100])

