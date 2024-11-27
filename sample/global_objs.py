from . import generator_config
from utils import file_utils

cofg = generator_config.sample_config

IndexDict = file_utils.read_line_dict(cofg['item_index_dict_path'], 3) if cofg['item_index_dict_path'] else None
FrequenceDict = file_utils.read_json(cofg['item_frequency_dict_path']) if cofg['item_index_dict_path'] else None
ParsedFeatureInfos = file_utils.read_json(cofg['item_feature_infos']) if cofg['item_feature_infos'] else None
