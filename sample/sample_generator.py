#parse input 2 json
'''
    sample format
    line_id \001 sample_type \001 0:label0;1:label1,.... \001 slot_id \001 fea_attr \002 fea_attr \002 ....

    hash slot   slotid -- fea_attr1,fea_attr2,fea_attr3
    embed slot  slotid -- 1.02,2.03..(emb_length)
    sample type 0 -- pos, 1 -- rand_neg, 2 -- poly_neg
'''
from . import generator_config
import simplejson as json
import global_objs


class Sample:
    def __init__(self, **spliter):
        self.line_id = 'default'
        self.label = {}
        self.sparse_feature = {}  #slot_id:fea
        self.fixed_sparse_feature = {}
        self.dense_feature = {}
        self.fixed_dense_feature = {}
        if spliter:
            if 'lv1_split' in spliter.keys():
                self.SPLIT_1 = spliter['lv1_split']
            else:
                self.SPLIT_1 = '\001'
            if 'lv2_split' in spliter.keys():
                self.SPLIT_2 = spliter['lv2_split']
            else:
                self.SPLIT_2 = '\002'
        self.sample_type = 0

    def format(self, lines: list):
        index_lis = [(lines.index(k), v) for k, v in self.label.items() if k in lines]
        index_lis.sort(key=lambda x: x[0])
        label_str = ';'.join(['{}:{}'.format(k, v) for k, v in index_lis])
        fixed_fea_str = [self.SPLIT_2.join(['{}:{}'.format(k, l) for l in v]) for k, v in self.fixed_sparse_feature.items()]
        fixed_dense_fea_str = ['{}:{}'.format(k, ','.join(v)) for k, v in self.fixed_dense_feature.items()]
        fea_str = [self.SPLIT_2.join(['{}:{}'.format(k, l) for l in v]) for k, v in self.sparse_feature.items()]
        dense_fea_str = ['{}:{}'.format(k, ','.join(v)) for k, v in self.dense_feature.items()]
        return self.SPLIT_1.join([self.line_id, label_str, self.sample_type, self.SPLIT_1.join(fixed_fea_str), fixed_dense_fea_str, self.SPLIT_1.join(fea_str), dense_fea_str])

    def parseFromStr(self, s, label_lines: list, dense_fea_lines: list = []):
        tmp_lis = s.split(self.SPLIT_1)
        self.line_id = tmp_lis[0]

        label_list = [x.split(':') for x in tmp_lis[1].split(';')]
        self.label = {label_lines[v[0]]: v[1] for v in label_list}
        fea_lis = tmp_lis[2:]
        for i in range(0, len(fea_lis), 2):
            if fea_lis[i] not in dense_fea_lines:
                self.feature[fea_lis[i]] = fea_lis[i + 1].split(self.SPLIT_2)
            else:
                self.feature[fea_lis[i]] = fea_lis[i + 1].split(',')

        return self


class SampleGenerator(object):
    def __init__(self):
        self.config = generator_config.generator_config
        self.sample_config = generator_config.sample_config

    def generatePosSample(self):
        sample = []
        return sample

    def generateNegSample(self, pos_sample: list):
        neg_sample = []
        return neg_sample

    def generate(self):
        samples = []
        samples = self.generatePosSample()
        samples = self.generateNegSample(samples)
        return samples

    def parse(self, s: str):
        lines = self.sample_config['label_headers']
        embed_slot_id = self.sample_config['embed_slot_id']
        sample = Sample()
        sample.parseFromStr(s, lines, embed_slot_id)
        return sample

    def saveSample(self):
        #save config
        #save sample
