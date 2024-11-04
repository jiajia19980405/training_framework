from . import generator_config
from utils import file_utils

cofg = generator_config.sample_config
FrequenceDict = None
if cofg['polynomial_sample_size'] != 0 and cofg['item_frequency_dict_path']:
    FrequenceDict = file_utils.read_json(cofg['item_frequency_dict_path'])

IndexDict = None
if cofg['item_index_dict_path']:
    IndexDict = file_utils.read_line_dict(cofg['item_index_dict_path'], 3)