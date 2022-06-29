# Utils

## Image augmentation

Sample image augmentation run

~~~bash
python utils/image\ augmentation/main.py --input ./data/in --output ./data/out --limit 150 --image-extensions png
~~~

## Xml2yolo

Sample Xml2yolo run

~~~bash
python utils/xml2yolo/main.py --input ./data/<classname> --output ./data/out --limit 150 --image-extensions png --width 410 --height 410
~~~
