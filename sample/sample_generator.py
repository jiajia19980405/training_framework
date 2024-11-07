#parse input 2 json
'''
    sample format
    line_id \001\001\001 0:label0;1:label1,.... \001\001\001 slot_id \001\001\001 fea_attr \002\002\002 fea_attr \002\002\002 ....

    hash slot   slotid -- fea_attr1,fea_attr2,fea_attr3
    embed slot  slotid -- 1.02,2.03..(emb_length)
'''
from . import generator_config
SPLIT_1 = generator_config['lv1_split']
SPLIT_2 = generator_config['lv2_split']
import simplejson as json
import global_objs

class Sample:
    def __init__(self):
        self.line_id = 'default'
        self.label = {}
        self.feature = {} #slot_id:fea
        self.dense_fea = {}

    def format(self, lines:list):
        index_lis = [(lines.index(k), v)for k,v in self.label.items() if k in lines]
        index_lis.sort(key=lambda x:x[0])
        label_str = ';'.join(['{}:{}'.format(k,v) for k,v in index_lis])
        fea_str = [SPLIT_2.join(['{}:{}'.format(k,l) for l in v]) for k, v in self.feature.items()]
        return SPLIT_1.join([self.line_id, label_str, SPLIT_1.join(fea_str)])


class SampleGenerator(object):
    def __init__(self):
        self.config = generator_config.sample_config
        pass

    def generatePosSample(self):
        sample = []
        return sample

    def generateNegSample(self, pos_sample:list):
        neg_sample = []
        return neg_sample

    def generate(self):
        samples = []
        samples = self.generatePosSample()
        samples = self.generateNegSample(samples)
        return samples

    def parse(self, s:str):
        tmp_lis = s.split(SPLIT_1)
        lines = self.config['label_headers']

        sample = Sample()
        sample.line_id = tmp_lis[0]

        label_list = [x.split(':') for x in tmp_lis[1].split(';')]
        sample.label = {lines[v[0]]: v[1] for v in label_list}

        fea_lis = tmp_lis[2:]
        for i in range(0,len(fea_lis),2):
            if fea_lis[i] not in self.config['embed_slot_id']:
                sample.feature[fea_lis[i]] = fea_lis[i+1].split(SPLIT_2)
            else:
                sample.feature[fea_lis[i]] = fea_lis[i+1].split(',')

        return sample

