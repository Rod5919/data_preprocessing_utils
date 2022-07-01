import json
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=True, help='input file')
    parser.add_argument('--output', '-o', type=str, required=True, help='output file')
    # Opening JSON file
    f = open(parser.parse_args().input)

    # returns JSON object as a dictionary
    data = json.load(f)

    # Closing file
    f.close()
    
    # Removing unwanted keys
    [x.pop('segmentation') for x in data['annotations']]
    
    # Removing unwanted categories
    data['annotations'] = [x for x in data['annotations'] if x['category_id'] == 1]

    # Writing to JSON file
    with open(parser.parse_args().output, 'w') as f:
        f.write(json.dumps(data, indent=4))    
