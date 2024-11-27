sample_config = {
    'lv1_split': '\001\001\001',
    'lv2_split': '\002\002\002',
    'label_headers': ['sim'],
    'feature_config': {
        'fixed_sparse_feature': [],
        'fixed_dense_feature': [],
        'sparse_feature': [],
        'dense_feature': []
    }
}

generator_config = {
    'polynomial_sample_size': 0,
    'item_frequency_dict_path': '',
    'random_neg_sample_size': 0
}


# name, slot_id, type, op_function, args(opt)
feature_dict = [
    ('pairs_hidden', 0, 'hidden', 'get_word_pairs',),
    ('first_entity_word', 1, 'fixed_sparse_feature', 'get_index_from_dict', 0, 'pairs_hidden'),
    ('second_entity_word', 2, 'sparse_feature', 'get_index_from_dict', 1, 'pairs_hidden'),
    ('first_entity_text_emb', 3, 'fixed_dense_feature', 'get_dense_from_dict', ),
    ('first_entity_text_emb', 4, 'dense_feature', 'get_dense_from_dict',),
]

for tup in feature_dict:
    if tup[2] in sample_config['feature_config']:
        sample_config['feature_config'][tup[2]].append(tup[1])
