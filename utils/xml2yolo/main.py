import argparse
from tqdm import tqdm
import glob
import os
import xml.etree.ElementTree as ET
import shutil

# OUT:
"""
{{classname}} x1 y1 w1 h1
{{classname}} x2 y2 w2 h2
"""

def return_bndboxes(filename):
    """ Returns a list of BoundingBoxesOnImage objects from an xml file. 

    Args:
        filename (str): The filename of the xml file.

    Returns:
        list: A list of BoundingBoxesOnImage objects.
    """    
    tree = ET.parse(filename)
    root = tree.getroot()
    bndboxes = []
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        if difficult == '0':
            bndbox = obj.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text
            bndboxes.append((int(xmin), int(ymin), int(xmax), int(ymax)))
    return bndboxes

def xml_to_yolo_bbox(bbox, w, h):
    # IN: xmin, ymin, xmax, ymax
    
    #reorganize bbox
    bbox = list(bbox)
    bbox[1], bbox[2] = bbox[2], bbox[1]
    # OUT: xmin, xmax, ymin, ymax
    
    x_center = ((bbox[1] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[2]) / 2) / h
    width = (bbox[1] - bbox[0]) / w
    height = (bbox[3] - bbox[2]) / h
    return " ".join((str(x_center), str(y_center), str(width), str(height)))

if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-I","--input_path", type=str, help="path to input images", default="data")
    parser.add_argument("-O","--output_path", type=str, help="path to output images", default="out")
    parser.add_argument("--limit", type=int, help="limit number of images to process", default=None)
    parser.add_argument("--image-extensions", type=str, help="image extensions to process", default="jpg")
    parser.add_argument("--width", type=int, help="width of the images", default=416)
    parser.add_argument("--height", type=int, help="height of the images", default=416)
    
    images = glob.glob(os.path.join(parser.parse_known_args()[0].input_path, f"*.{parser.parse_known_args()[0].image_extensions}"))
    annotations = glob.glob(os.path.join(parser.parse_known_args()[0].input_path, f"*.xml"))
    
    images.sort()
    annotations.sort()
    
    classname = parser.parse_known_args()[0].input_path.split(os.sep)[-2]
    for image, annotation in zip(images[:parser.parse_known_args()[0].limit], annotations[:parser.parse_known_args()[0].limit]):
        bboxes = return_bndboxes(annotation)
        
        print(image)
        print(annotation)
        txt = ""
        
        for bbox in bboxes:
            txt += "{{ "+str(classname)+" }} "
            txt += xml_to_yolo_bbox(bbox, parser.parse_known_args()[0].width, parser.parse_known_args()[0].height)
            txt += "\n"
        
        shutil.copy(image, os.path.join(parser.parse_known_args()[0].output_path, os.path.basename(image)))
        with open(os.path.join(parser.parse_known_args()[0].output_path, os.path.basename(annotation).replace(".xml", ".txt")), "w") as f:
            f.write(txt)
        
    