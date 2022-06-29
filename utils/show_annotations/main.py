import cv2
import argparse
import glob
import os
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

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

def draw_bndboxes(image, bndboxes, color=(0, 255, 0), thickness=2):
    """ Returns a list of BoundingBoxesOnImage objects from an xml file.

    Args:
        image (np.ndarray): An image.
        bndboxes (list): A list of BoundingBoxes
        color (tuple, optional): Bounding boxes color. Defaults to (0, 255, 0).
        thickness (int, optional): Bounding boxes line thickness. Defaults to 2.

    Returns:
        np.ndarray: An image with bounding boxes drawn.
    """    
    for bndbox in bndboxes:
        xmin, ymin, xmax, ymax = bndbox
        image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, thickness)
    return image

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-I","--input_path", type=str, help="path to input images", default="data")
    parser.add_argument("--image-extensions", type=str, help="image extensions to process", default="jpg")
    parser.add_argument("--window-size", nargs=2, type=int, help="window size", default=(416, 416))
    
    image_files = glob.glob(parser.parse_known_args()[0].input_path + f"/*.{parser.parse_known_args()[0].image_extensions}")
    annotations = glob.glob(parser.parse_known_args()[0].input_path + f"/*.xml")
    
    image_files.sort()
    annotations.sort()
    
    print(parser.parse_known_args()[0].window_size)
    plt.rcParams["figure.figsize"] = parser.parse_known_args()[0].window_size
    
    for image_file, annotation, plt_index in zip(image_files, annotations, (331, 332, 333, 334, 335, 336, 337, 338, 339)):
        bboxes = return_bndboxes(annotation)
        image = draw_bndboxes(cv2.imread(image_file), bboxes)
        
        plt.subplot(plt_index), plt.imshow(image), plt.title(image_file.split("/")[-1][:15])
        plt.xticks([]), plt.yticks([])
    plt.show()
        