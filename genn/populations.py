# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 19:01:01 2014

@author: micha
"""

from PyNN import common
from . import simulator
from pyNN.standardmodels import StandardCellType
from pyNN.parameters import ParameterSpace, simplify
from .recording import Recorder

class Assembly(common.Assembly):
    _simulator = simulator


class PopulationView(common.PopulationView):
    _assembly_class = Assembly
    _simulator = simulator

    def _get_parameters(self, *names):
        """
        return a ParameterSpace containing native parameters
        """
        pass
    
    def _set_parameters(self, parameter_space):
        """
        parameter_space should contain native parameters
        """
        pass
    
    def _set_initial_value_array(self, variable, initial_values):
        raise NotImplementedError
        
    def _get_view(self, selector, label=None):
        return PopulationView(self, selector, label)
        

class Population(common.Population):
    __doc__ = common.Population.__doc__
    _simulator = simulator
    _recorder_class = Recorder
    _assembly_class = Assembly

    def _create_cells(self):
        pass
    
    def _set_initial_value_array(self, variable, value):
        pass

    def _get_view(self, selector, label=None):
        return PopulationView(self, selector, label)            
    
    def _get_parameters(self, *names):
        """
        return a ParameterSpace containing native parameters
        """
        parameter_dict = {}
        for name in names:
            value = simplify(getattr(self.brian_group, name))
            parameter_dict[name] = value
        return ParameterSpace(parameter_dict, shape=(self.size,))
        
    def _set_parameters(self, parameter_space):
        """parameter_space should contain native parameters"""
        parameter_space.evaluate(simplify=False)
        for name, value in parameter_space.items():
            setattr(self.brian_group, name, value)