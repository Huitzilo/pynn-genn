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
    pass

class Population(common.Population):
    def _create_cells(self):
        #TODO
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

