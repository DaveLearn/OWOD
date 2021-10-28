import os
import random
import itertools
dset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../VOC2007/ImageSets/Main'))
input_file = os.path.join(dset_path, 't4_ft_300.txt')
output_file = os.path.join(dset_path, 't4_ft_100.txt')

with open(input_file, "r") as inf:
    input_items = inf.readlines()

random.shuffle(input_items)
num_of_images = len(input_items)

num_of_subsample = num_of_images // 3
subsample = input_items[:num_of_subsample]

# build same size list but from subset of actual data
output_items = [subsample[i % num_of_subsample] for i in range(num_of_images)]

with open(output_file, "w+") as outf:
    outf.writelines(output_items)

