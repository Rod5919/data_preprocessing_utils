import fiftyone.zoo as foz

# To download the COCO dataset for only the "person" class
dataset = foz.load_zoo_dataset(
    "coco-2017",
    split="train", #validaion
    label_types= "detections",
    classes=["person"],
    max_samples=5000,
)