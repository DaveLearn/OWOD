import random

percent_to_keep = 25


def create_dataset(train_file, dest_file):
   
    with open(train_file, mode="r") as tf:
        file_names = tf.readlines()

    random.shuffle(file_names)

    to_keep = int(len(file_names) * (percent_to_keep / 100))

    with open(dest_file, "x") as df:
        df.writelines(file_names[:to_keep])
    
    print('Saved to file: ' + dest_file)


for task_num in range(1,5):
    create_dataset(f"/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/t{task_num}_train.txt", f"/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/t{task_num}_{percent_to_keep}pct_train.txt")

