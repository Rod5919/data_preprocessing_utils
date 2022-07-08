import shutil
import random
import glob
from tqdm import tqdm
import argparse
import os

def folder_generator(folder_path):
    files = glob.glob(folder_path + "/*.jpg")
    random.shuffle(files)
    for image_path in files:
        yield image_path
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_path', nargs='+', type=str, help='Path to the folder containing items')
    parser.add_argument('--train_path', type=str, help='Path to the folder to save train items')
    parser.add_argument('--test_path', type=str, help='Path to the folder to save test items')
    parser.add_argument('--valid_path', type=str, help='Path to the folder to save valid items')
    
    folders = parser.parse_args().folder_path
    
    for folder_path in folders:
        count = 0
        train_path = parser.parse_args().train_path
        test_path = parser.parse_args().test_path
        valid_path = parser.parse_args().valid_path
        
        if not os.path.exists(train_path):
            os.makedirs(train_path)
        if not os.path.exists(test_path):
            os.makedirs(test_path)
        if not os.path.exists(valid_path):
            os.makedirs(valid_path)
        
        number_of_files = len(glob.glob(folder_path + "/*.jpg"))
        for i in tqdm(folder_generator(folder_path)):
            if count < number_of_files * 0.8:
                try:
                    shutil.copy(i[:-3]+"txt", train_path)
                    shutil.copy(i, train_path)
                except:
                    print("File not moved")
            elif count < number_of_files * 0.9:
                try:
                    shutil.copy(i[:-3]+"txt", test_path)
                    shutil.copy(i, test_path)
                except:
                    print("File not moved")
            else:
                try:
                    shutil.copy(i[:-3]+"txt", valid_path)
                    shutil.copy(i, valid_path)
                except:
                    print("File not moved")
            count += 1
    print("Done!")