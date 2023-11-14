import glob
import os, shutil
import random
# label文件的路径
label_path = '/mnt/d/workspace/data/ZDSpassengerflow/yolo/'
image_path = '/mnt/d/workspace/data/ZDSpassengerflow/'

#接下来是写入txt文件中
if __name__ == '__main__':
    split_rate = 0.8
    file_list = os.listdir(label_path)
    train_num = int(len(file_list)*split_rate)
    val_num = int(len(file_list)-train_num)
    random.shuffle(file_list)
    train_file = file_list[:train_num]
    val_file = file_list[train_num:]
    os.mkdir(image_path+'/images')
    os.mkdir(image_path + '/labels')

    #存放训练集
    os.mkdir(image_path + '/images/train')
    os.mkdir(image_path + '/labels/train')
    for file in train_file:
        shutil.copy(image_path+file[:-4]+'.jpg', image_path + '/images/train/'+file[:-4]+'.jpg')
        shutil.copy(label_path + file, image_path + '/labels/train/' + file)

    # 存放训练集
    os.mkdir(image_path + '/images/val')
    os.mkdir(image_path + '/labels/val')
    for file in train_file:
        shutil.copy(image_path + file[:-4] + '.jpg', image_path + '/images/val/' + file[:-4] + '.jpg')
        shutil.copy(label_path + file, image_path + '/labels/val/' + file)


