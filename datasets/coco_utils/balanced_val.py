import itertools
import random
import os
import xml.etree.ElementTree as ET
from fvcore.common.file_io import PathManager

from detectron2.utils.store_non_list import Store

VOC_CLASS_NAMES_COCOFIED = [
    "airplane",  "dining table", "motorcycle",
    "potted plant", "couch", "tv"
]

BASE_VOC_CLASS_NAMES = [
    "aeroplane", "diningtable", "motorbike",
    "pottedplant",  "sofa", "tvmonitor"
]

VOC_CLASS_NAMES = [
    "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat",
    "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person",
    "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

T2_CLASS_NAMES = [
    "truck", "traffic light", "fire hydrant", "stop sign", "parking meter",
    "bench", "elephant", "bear", "zebra", "giraffe",
    "backpack", "umbrella", "handbag", "tie", "suitcase",
    "microwave", "oven", "toaster", "sink", "refrigerator"
]

T3_CLASS_NAMES = [
    "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
    "banana", "apple", "sandwich", "orange", "broccoli",
    "carrot", "hot dog", "pizza", "donut", "cake"
]

T4_CLASS_NAMES = [
    "bed", "toilet", "laptop", "mouse",
    "remote", "keyboard", "cell phone", "book", "clock",
    "vase", "scissors", "teddy bear", "hair drier", "toothbrush",
    "wine glass", "cup", "fork", "knife", "spoon", "bowl"
]

UNK_CLASS = ["unknown"]

items_per_class = 45

# Change this accodingly for each task t*
known_classes = [ list(itertools.chain(VOC_CLASS_NAMES)), \
                list(itertools.chain(VOC_CLASS_NAMES, T2_CLASS_NAMES)) , \
                list(itertools.chain(VOC_CLASS_NAMES, T2_CLASS_NAMES, T3_CLASS_NAMES)), \
                list(itertools.chain(VOC_CLASS_NAMES, T2_CLASS_NAMES, T3_CLASS_NAMES, T4_CLASS_NAMES)) ]

train_file = '/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/all_task_val.txt'

dest_files = [ '/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/t1_val_' + str(items_per_class) + '.txt', \
               '/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/t2_val_' + str(items_per_class) + '.txt', \
               '/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/t3_val_' + str(items_per_class) + '.txt' ]

# known_classes = list(itertools.chain(VOC_CLASS_NAMES))
# train_files = ['/home/fk1/workspace/OWOD/datasets/VOC2007/ImageSets/Main/train.txt']
annotation_location = '/home/n11020211/OWOD/datasets/VOC2007/Annotations'

file_names = []

with open(train_file, mode="r") as myFile:
    file_names.extend(myFile.readlines())

random.shuffle(file_names)

for task_num in range(3):
    print(f"known classes: {','.join(known_classes[task_num])} ")
    wanted_unknowns = len(known_classes[task_num]) * items_per_class
    print(f"wanted unknowns: {wanted_unknowns}")

    image_store = Store(len(known_classes[task_num]), items_per_class)
    unknown_store = Store(1, wanted_unknowns)

    current_min_item_count = 0

    for fileid in file_names:
        fileid = fileid.strip()
        anno_file = os.path.join(annotation_location, fileid + ".xml")

        with PathManager.open(anno_file) as f:
            tree = ET.parse(f)

        for obj in tree.findall("object"):
            cls = obj.find("name").text
            if cls in VOC_CLASS_NAMES_COCOFIED:
                cls = BASE_VOC_CLASS_NAMES[VOC_CLASS_NAMES_COCOFIED.index(cls)]
            if cls in known_classes[task_num]:
                image_store.add((fileid,), (known_classes[task_num].index(cls),))
            else:
                unknown_store.add((fileid,), (0, ))

        current_min_item_count = min([len(items) for items in image_store.retrieve(-1)])
        current_unknown_count = len(unknown_store.retrieve(0))
        print(f'known_min={current_min_item_count}, unknown={current_unknown_count}')
        
        if current_min_item_count >= items_per_class and current_unknown_count >= wanted_unknowns:
            break

    filtered_file_names = unknown_store.retrieve(0)
    for items in image_store.retrieve(-1):
        filtered_file_names.extend(items)
    
    print(image_store)
    print(unknown_store)
    print(len(filtered_file_names))
    print(len(set(filtered_file_names)))

    filtered_file_names = set(filtered_file_names)
    filtered_file_names = map(lambda x: x + '\n', filtered_file_names)

    with open(dest_files[task_num], mode="w") as myFile:
        myFile.writelines(filtered_file_names)

    print('Saved to file: ' + dest_files[task_num])
