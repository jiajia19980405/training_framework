#parse input 2 json
'''
    sample format
    line_id \001\001\001 0:label0,1:label1,.... \001\001\001 slot_id \001\001\001 fea_attr \002\002\002 fea_attr \002\002\002 ....

    hash slot   slotid -- fea_attr1,fea_attr2,fea_attr3
    embed slot  slotid -- 1.02,2.03..(emb_length)
'''
from . import generator_config
SPLIT_1 = generator_config['lv1_split']
SPLIT_2 = generator_config['lv2_split']
import simplejson as json

class Sample:
    def __init__(self):
        self.label = {}
        self.feature = {} #slot_id:fea

    def format(self, lines:list):
        index_lis = [(lines.index(k), v)for k,v in self.label.items() if k in lines]
        index_lis.sort(key=lambda x:x[0])
        label_str = ';'.join(['{}:{}'.format(k,v) for k,v in index_lis])
        return SPLIT_1.join([])


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


