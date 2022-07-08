import os
import shutil
from tqdm import tqdm

def directory_generator(directory):
    """
    Generates a list of files in a directory.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                yield os.path.join(root, file)

def write_yolo_annotation(file_path, lines):
    """
    Writes the yolo annotation file.
    """
    with open(file_path, 'w') as f:
        f.write(lines)
        
def read_txt_file(file_path, filter):
    """
    Reads a txt file.
    """
    with open(file_path, 'r') as f:
        if filter:
            return "".join(set([line for line in f.readlines() if line.startswith(filter)]))
        
def copy_image(file_path, new_directory):
    """
    Copies an image to a new directory.
    """
    shutil.copy(file_path, new_directory)


if __name__ == '__main__':
    input_dirs = [
        "out/People",
        "out/Pistols",
        "out/Knifes",
    ]
    output_paths = [
        "filtered/People",
        "filtered/Pistols",
        "filtered/Knifes",
    ]
    filters = [str(x) for x in range(0, 3)]
    for input_dir, output_path, filter_class in zip(input_dirs, output_paths, filters):
        print("Processing: {}...".format(input_dir))
        for file_path in tqdm(directory_generator(input_dir)):
            write_yolo_annotation(os.path.join(output_path, os.path.basename(file_path)), read_txt_file(file_path, filter_class))
            copy_image(file_path[:-4] + '.jpg', os.path.join(output_path, os.path.basename(file_path[:-4] + '.jpg')))
            
    print('Done!')