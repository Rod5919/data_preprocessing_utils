import os
import shutil

def directory_generator(path):
    """ Generates a list of all files in a directory

    Args:
        path (str): path to the directory to generate files

    Yields:
        str: path to the files
    """    
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)
            
def remove_image_without_annotation(image_file):
    """Removes an image if it doesn't have an annotation    

    Args:
        image_file (str): path to the image file

    """    
    annotation = image_file[:-4] + ".txt"
    if not (os.path.exists(image_file)):
        shutil.rmtree(image_file)
    
if __name__ == "__main__":
    [remove_image_without_annotation(image_file) for image_file in directory_generator("/home/ubuntu/data/train/images")]