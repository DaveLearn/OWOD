import os
import random
import itertools
dset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../VOC2007/ImageSets/Main'))
input_file = os.path.join(dset_path, 't4_ft_100.txt')
match_file = os.path.join(dset_path, 't4_ft_300.txt' )
output_file = os.path.join(dset_path, 't4_ft_100ss.txt')

with open(match_file, "r") as inf:
    items = inf.readlines()

num_items_needed = len(items)

with open(input_file, "r") as inf:
    input_items = inf.readlines()

random.shuffle(input_items)
num_of_input = len(input_items)


# build same size list but from subset of actual data
output_items = [input_items[i % num_of_input] for i in range(num_items_needed)]

with open(output_file, "w+") as outf:
    outf.writelines(output_items)

