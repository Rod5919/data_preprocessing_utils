import argparse
import numpy as np
import imgaug as ia
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import glob
import os
import cv2
import random
from tqdm import tqdm
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
        bndbox = obj.find('bndbox')
        xmin = bndbox.find('xmin').text
        ymin = bndbox.find('ymin').text
        xmax = bndbox.find('xmax').text
        ymax = bndbox.find('ymax').text
        bndboxes.append((int(xmin), int(ymin), int(xmax), int(ymax)))
    return bndboxes

ia.seed(1)

seq = iaa.Sequential([
    iaa.Fliplr(0.5), # horizontal flips
    iaa.Crop(percent=(0, 0.05)), # random crops
    # Small gaussian blur with random sigma between 0 and 0.5.
    # But we only blur about 50% of all images.
    iaa.Sometimes(
        0.5,
        iaa.GaussianBlur(sigma=(0, 0.5))
    ),
    # Strengthen or weaken the contrast in each image.
    iaa.LinearContrast((0.75, 1.5)),
    # Add gaussian noise.
    # For 50% of all images, we sample the noise once per pixel.
    # For the other 50% of all images, we sample the noise per pixel AND
    # channel. This can change the color (not only brightness) of the
    # pixels.
    iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
    # Make some images brighter and some darker.
    # In 20% of all cases, we sample the multiplier once per channel,
    # which can end up changing the color of the images.
    iaa.Multiply((0.8, 1.2), per_channel=0.2),
    # Apply affine transformations to each image.
    # Scale/zoom them, translate/move them, rotate them and shear them.
    iaa.Affine(
        scale={"x": (0.6, 1.2), "y": (0.6, 1.2)},
        translate_percent={"x": (-0.1, 0.1), "y": (-0.1, 0.1)},
        rotate=(-10, 10)
    )
], random_order=True) # apply augmenters in random order

def augmenting_images(images, xml_files):
    """ Augment images and xml files

    Args:
        images (list): images to be augmented
        xml_files (listen): annotations of images

    Returns:
        lists: images and xml_files after augmentation
    """
    images_aug = []
    bbs_aug = []
    for image,bbs_file in tqdm(zip(images,xml_files)):
        bndboxes = []
        for i in return_bndboxes(filename=bbs_file):
            bndboxes.append(BoundingBox(x1=i[0], y1=i[1], x2=i[2], y2=i[3]))
        bbs = BoundingBoxesOnImage(bndboxes, shape=image.shape)
        image_aug_aux, bbs_aug_aux = seq(image=image, bounding_boxes=bbs)
        images_aug.append(image_aug_aux)
        bbs_aug.append(bbs_aug_aux)
    return images_aug, bbs_aug
  
def writexmlfilewithnewbndboxes(xml_file, bbs_aug, output_path):
    """ Writes an xml file with new bounding boxes.

    Args:
        xml_file (str): The xml file to write
        bbs_aug (list): List of bounding boxes_description_file
        output_path (str): The path to save the new xml file
    """    
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for obj,bbs in zip(root.iter('object'),bbs_aug.bounding_boxes):
        difficult = '0'
        bndbox = obj.find('bndbox')
        if difficult == '0':
            bndbox.find('xmin').text = str(int(bbs.x1))
            bndbox.find('xmax').text = str(int(bbs.x2))
            bndbox.find('ymin').text = str(int(bbs.y1))
            bndbox.find('ymax').text = str(int(bbs.y2))
    try:
        tree.write(output_path)
    except:
        with open(output_path, 'w') as f:
            f.write(tree.tostring(et, encoding='utf8', method='xml'))
    
def save_data(images_aug, xml_files, bbs_aug, parser):
    """ Saves the augmented data.

    Args:
        images_aug (list): images after augmentation
        xml_files (list): xml files after augmentation
        bbs_aug (list): bounding boxes after augmentation
        parser (parser): parser with the arguments
    """    
    for i, (image_aug, xml_file, bbs) in enumerate(zip(images_aug, xml_files, bbs_aug)):
        cv2.imwrite(os.path.join(parser.parse_known_args()[0].output_path, f"imagev{parser.parse_known_args()[0].version}_{i}.jpg"),image_aug);
        writexmlfilewithnewbndboxes(xml_file, bbs, os.path.join(parser.parse_known_args()[0].output_path, f"imagev{parser.parse_known_args()[0].version}_{i}.xml"))
        
if __name__ == '__main__':
    # Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-I","--input_path", type=str, help="path to input images", default="data")
    parser.add_argument("-O","--output_path", type=str, help="path to output images", default="out")
    parser.add_argument("--limit", type=int, help="limit number of images to process", default=None)
    parser.add_argument("--image-extensions", type=str, help="image extensions to process", default="jpg")
    parser.add_argument("--version", type=int, help="version", default=1)
    
    print("Getting image files...")
    image_files = [x for x in tqdm(glob.glob(os.path.join(parser.parse_known_args()[0].input_path,f"*.{parser.parse_known_args()[0].image_extensions}")))]
    random.shuffle(image_files)
    
    print("Reading annotations...")
    xml_files = ["/".join(image_file.split("/")[:-1])+'/'+image_file.split("/")[-1][:-len(parser.parse_known_args()[0].image_extensions)]+"xml"for image_file in tqdm(image_files)]
    
    print("Reading images...")
    images = [cv2.imread(image_file) for image_file in tqdm(image_files[:parser.parse_known_args()[0].limit])]

    # Augment images
    print("Augmenting images...")
    images_aug, bbs_aug = augmenting_images(images, xml_files)
    
    # Save images
    print("Saving images...")
    save_data(images_aug, xml_files, bbs_aug, parser)
    
        
