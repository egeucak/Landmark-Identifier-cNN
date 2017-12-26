import os
import math
import random
import shutil

location = 'C:/Users/Mavi/PycharmProjects/wc/photographs/Yeni klasör TMM/'

def recursiveDir(base_location,location,ratio): #gets image paths

    for file in os.listdir(location):
        new_location = location+file
        if ('.jpg' not in file):
            rec_imagePaths = (recursiveDir(base_location,new_location+'/',ratio))
            split_data(base_location,new_location+'/',ratio)

def split_data(base_location,location, ratio):
    imagePaths = []
    location_name = location.split('/')[-2]
    base_location_name = '/'.join(base_location.split('/')[:-1])
    for file in os.listdir(location):
        imagePaths.append(location+file)

    random.shuffle(imagePaths)
    test_size = math.ceil(len(imagePaths)*ratio)

    test_data = imagePaths[:test_size]
    train_data = imagePaths[test_size:]

    create_train_test_dirs(base_location_name)
    copy_files(test_data,base_location_name+'_test/')
    copy_files(train_data,base_location_name+'_train/')

def create_train_test_dirs(location):
    train_directory = os.path.dirname(location+'_train/')
    if not os.path.exists(train_directory):
        os.makedirs(train_directory)

    test_directory = os.path.dirname(location+'_test/')
    if not os.path.exists(test_directory):
        os.makedirs(test_directory)

def copy_files(paths,target_path):
    label = paths[0].split('/')[-2]
    if not os.path.exists(target_path+label+'/'):
        os.makedirs(target_path+label+'/')
    for path in paths:
        file_name = path.split('/')[-1]
        shutil.copy2(path,target_path+label+'/'+file_name)

paths = recursiveDir(location,location,0.2)
