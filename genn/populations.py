# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 19:01:01 2014

@author: micha
"""

from PyNN import common
from pyNN.parameters import ParameterSpace
from . import simulator

class IDMixin(common.IDMixin):
    pass

class BasePopulation(common.BasePopulation):
    def get(self, parameter_names, gather=False):
        pass
    
    def set(self, **parameters):
        pass
    
    def initialize(self, **initial_values):
        pass
    

class Population(common.Population):
    
    def _recorder_class(self):
        # needs to return a recorder
        pass
    
    def _create_cells(self):
        # number of neurons is in self.size
        # parameterised cell class is in self.celltype
        # name is in self.label
        # need to provide something for self._recorder_class
        # need to create array self.all_cells
        pass

    def initialize(self, **initial_values):
        #initial_values is a dict
        pass
    
    def _get_parameters(self):
        #TODO
        pass
    
    def _set_parameters(self):
        #TODO
        pass
    
    def _get_view(self):
        #TODO
        pass

class PopulationView(common.PopulationView):
    pass

class Assembly(common.Assembly):
    pass

