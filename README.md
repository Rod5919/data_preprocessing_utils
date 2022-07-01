# Utils

## Image augmentation

Sample image augmentation run

~~~bash
python utils/image\ augmentation/main.py --input ./data/in --output ./data/out --limit 150 --image-extensions png
~~~

## Xml2yolo

Sample Xml2yolo run

~~~bash
python utils/xml2yolo/main.py --input ./data/<classname>/<train, test or valid> --output ./data/out --limit 150 --image-extensions png --width 410 --height 410
~~~

## ShowAnnotations

Sample show_annotations

~~~bash
python utils/show_annotations/main.py --input ./data/<classname>/<train, test or valid> --output ./data/out --limit 150 --image-extensions png --width 410 --height 410
~~~

## To download the COCO dataset
[Official Documentation](https://voxel51.com/docs/fiftyone/integrations/coco.html#coco) and sample code...

~~~python
import fiftyone.zoo as foz

# To download the COCO dataset for only the "person" class
dataset = foz.load_zoo_dataset(
    "coco-2017",
    split="train", #validaion
    label_types=["detections", "segmentations"],
    classes=["person"],
    max_samples=4000,
)

~~~

## filter segmentations

~~~bash
python utils/filter_segmentation/main.py --input <json_file> --output <json_file>
~~~
