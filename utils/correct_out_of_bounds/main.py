import os
from tqdm import tqdm

def folder_generator(path: str) -> str:
    """ Generates a list of all folders in a directory

    Args:
        path (str): Path to the directory

    Returns:
        str: List of all folders in the directory

    Yields:
        Iterator[str]: Iterator of all folders in the directory
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            yield os.path.join(root, file)
            
def get_bounding_boxes(path: str) -> list:
    """ Generates a list of all bounding boxes in a file

    Args:
        path (str): Path to the file

    Returns:
        list: List of all bounding boxes in the file
    """    
    with open(path, 'r') as f:
        lines = f.readlines()
        bounding_boxes = []
        for line in lines:
            bounding_boxes.append(line.split(' '))
        return bounding_boxes
    
def convert_yolo_to_pascal_voc(bounding_boxes: list) -> list:
    """ Converts bounding boxes in yolo to pascal

    Args:
        bounding_boxes (list): List of bounding boxes in yolo format

    Returns:
        list: List of bounding boxes in pascal format
    """    
    pascal_voc_bounding_boxes = []
    for bounding_box in bounding_boxes:
        class_id = int(bounding_box[0])
        xmin = float(bounding_box[1]) - float(bounding_box[3])/2
        ymin = float(bounding_box[2]) - float(bounding_box[4])/2
        xmax = float(bounding_box[1]) + float(bounding_box[3])/2
        ymax = float(bounding_box[2]) + float(bounding_box[4])/2
        pascal_voc_bounding_boxes.append([class_id, xmin, ymin, xmax, ymax])
    return correct_out_bounds(pascal_voc_bounding_boxes, 416, 416)

def correct_out_bounds(bounding_boxes: list, image_width: int, image_height: int) -> list:
    """ Corrects bounding boxes that are out of bounds

    Args:
        bounding_boxes (list): List of bounding boxes in pascal format
        image_width (int): Width of the image
        image_height (int): Height of the image

    Returns:
        list: List of bounding boxes in pascal format with corrected bounds
    """    
    for index, bounding_box in enumerate(bounding_boxes):
        if bounding_box[1] < 0:
            bounding_box[1] = 0
        if bounding_box[2] < 0:
            bounding_box[2] = 0
        if bounding_box[3] > image_width:
            bounding_box[3] = image_width
        if bounding_box[4] > image_height:
            bounding_box[4] = image_height
        bounding_boxes[index] = bounding_box
    return bounding_boxes

def bounding_boxes_to_string(bounding_boxes: list) -> str:
    """ Converts a list of bounding boxes to a string

    Args:
        bounding_boxes (list): List of bounding boxes in yolo format

    Returns:
        str: String of bounding boxes in yolo format
    """    
    bounding_boxes_string = ''
    for bounding_box in bounding_boxes:
        bounding_boxes_string += " ".join((str(x) for x in bounding_box)) + "\n"
    return bounding_boxes_string

def save_bounding_boxes(bounding_boxes: list, path: str):
    """ Saves a list of bounding boxes to a file

    Args:
        bounding_boxes (list): List of bounding boxes in yolo format
        path (str): Path to the file to save the bounding boxes
    """    
    with open(path, 'w') as f:
        f.write(bounding_boxes_to_string(bounding_boxes))

if __name__ == '__main__':
    [save_bounding_boxes(convert_yolo_to_pascal_voc(get_bounding_boxes(path)), os.path.join("/home/rodri/Documents/data_preprocessing_utils/datasetv4/Knifes/labels", os.path.basename(path))) for path in tqdm(folder_generator('/home/rodri/Documents/data_preprocessing_utils/datasetv3/classes/Knifes/labels'))]
    [save_bounding_boxes(convert_yolo_to_pascal_voc(get_bounding_boxes(path)), os.path.join("/home/rodri/Documents/data_preprocessing_utils/datasetv4/People/labels", os.path.basename(path))) for path in tqdm(folder_generator('/home/rodri/Documents/data_preprocessing_utils/datasetv3/classes/People/labels'))]
    [save_bounding_boxes(convert_yolo_to_pascal_voc(get_bounding_boxes(path)), os.path.join("/home/rodri/Documents/data_preprocessing_utils/datasetv4/Pistols/labels", os.path.basename(path))) for path in tqdm(folder_generator('/home/rodri/Documents/data_preprocessing_utils/datasetv3/classes/Pistols/labels'))]