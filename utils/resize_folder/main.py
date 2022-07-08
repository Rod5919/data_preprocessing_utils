import os
from tqdm import tqdm

def folder_generator(folder_path):
    print(folder_path)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".jpg"):
                print(file)
                yield os.path.join(root, file)

def xml_to_yolo_bbox(bbox, w, h):
    # IN: xmin, ymin, xmax, ymax
    
    #reorganize bbox
    bbox = list(bbox)
    bbox[1], bbox[2] = bbox[2], bbox[1]
    # augmented: xmin, xmax, ymin, ymax
    
    x_center = ((bbox[1] + bbox[0]) / 2) / w
    y_center = ((bbox[3] + bbox[2]) / 2) / h
    width = (bbox[1] - bbox[0]) / w
    height = (bbox[3] - bbox[2]) / h
    return " ".join((str(x_center), str(y_center), str(width), str(height)))

def xml2yolo(xml_path, augmentedput_path, classnum, width, height):
    from lxml import etree
    tree = etree.parse(xml_path)
    root = tree.getroot()
    for child in root:
        if child.tag == 'object':
            for grandchild in child:
                if grandchild.tag == 'name':
                    name = grandchild.text
                    classnum = 2 if name == 'knife' else 0
                if grandchild.tag == 'bndbox':
                    for greatgrandchild in grandchild:
                        if greatgrandchild.tag == 'xmin':
                            xmin = int(greatgrandchild.text)
                        if greatgrandchild.tag == 'ymin':
                            ymin = int(greatgrandchild.text)
                        if greatgrandchild.tag == 'xmax':
                            xmax = int(greatgrandchild.text)
                        if greatgrandchild.tag == 'ymax':
                            ymax = int(greatgrandchild.text)
                    augmentedput_file = open(augmentedput_path, 'a')
                    augmentedput_file.write(str(classnum) + " " + xml_to_yolo_bbox((xmin, ymin, xmax, ymax), width, height) + "\n")
                    augmentedput_file.close()
            
def resize_image(image_path, new_width, new_height, augmentedput_path):
    from PIL import Image
    img = Image.open(image_path)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    img.save(augmentedput_path)
    
if __name__ == '__main__':
    # Faces
    for image_path in tqdm(folder_generator('/home/rodri/Documents/data_preprocessing_utils/datasetv3/People')):
        resize_image(
            image_path,
            416,
            416,
            os.path.join("/home/rodri/Documents/data_preprocessing_utils/datasetv3/resized_people", image_path.split(os.sep)[-1])
        )
    
        xml_path = image_path[:-3]+"xml"
        xml2yolo(
            xml_path,
            os.path.join("/home/rodri/Documents/data_preprocessing_utils/datasetv3/resized_people", xml_path.split(os.sep)[-1][:-3] + "txt"),
            0,
            416,
            416
        )