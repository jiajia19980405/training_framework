#parse input 2 json
'''
    sample format
    line_id \001\001\001 0:label0,1:label1,.... \001\001\001 slot_id \001\001\001 fea_attr \002\002\002 fea_attr \002\002\002 ....

    hash slot   slotid -- fea_attr1,fea_attr2,fea_attr3
    embed slot  slotid -- 1.02,2.03..(emb_length)
'''

import simplejson as json
from . import generator_config
class SampleGenerator(object):
    def __init__(self):
        self.config = generator_config.sample_config
        pass

    def generatePosSample(self):
        sample = []
        return sample

    def generateNegSample(self, pos_sample:list):


    def generate(self):
        samples = []
        samples = generatePosSample()
        samples = generateNegSample()
        return samples


