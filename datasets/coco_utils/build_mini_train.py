import random

percent_to_keep = 75

def create_dataset(train_file, dest_file):
   
    with open(train_file, mode="r") as tf:
        file_names = tf.readlines()

    random.shuffle(file_names)

    to_keep = len(file_names) * percent_to_keep // 100

    with open(dest_file, "x") as df:
        df.writelines(file_names[:to_keep])
    
    print('Saved to file: ' + dest_file)


create_dataset(f"/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/all_task_val.txt", f"/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/all_task_val_{percent_to_keep}pct.txt")

