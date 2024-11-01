import simplejson as json
import os

def read_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def read_line_dict(file_path, num:int = 3):
    with open(file_path, 'r') as f:
        lis = f.readlines()

    for i in range(len(lis)):

    return [l.split('\t') for l in lis if len(l.split('\t')) == num]