import simplejson as json
import os

def read_json(json_file):
    with open(json_file, 'r') as f:
        return json.load(f)

def read_line_dict(file_path, num:int = 3):
    with open(file_path, 'r') as f:
        lis = f.readlines()

    res = []
    cannot_parse_lis = []
    for i in range(len(lis)):
        line = lis[i].split('\t')
        if len(line) == num:
            res.append(line)
        else:
            cannot_parse_lis.append(lis[i])
    return res, cannot_parse_lis
