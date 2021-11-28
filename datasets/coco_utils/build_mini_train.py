import random
task_num = 4
num_to_keep = 2566


def create_dataset(train_file, dest_file):
   
    with open(train_file, mode="r") as tf:
        file_names = tf.readlines()

    random.shuffle(file_names)

    to_keep = num_to_keep

    with open(dest_file, "x") as df:
        df.writelines(file_names[:to_keep])
    
    print('Saved to file: ' + dest_file)



create_dataset(f"/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/t{task_num}_train.txt", f"/home/n11020211/OWOD/datasets/VOC2007/ImageSets/Main/t{task_num}_ft_unbalanced.txt")

