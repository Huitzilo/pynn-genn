# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 22:51:42 2014

@author: micha
"""
import pyNN.recording 

class Recorder(pyNN.recording.Recorder):
    
    def _record(self, variable, new_ids, sampling_interval):
        pass
    
    def _reset(self):
        pass
    
    def get(self, variables, gather=False, filter_ids=None, clear=False,
            annotations=None):
        pass
    
    def clear(self):
        pass
    
    def count(self, variable, gather=True, filter_ids=None):
        pass
