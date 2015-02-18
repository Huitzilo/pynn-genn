# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 12:20:43 2015

@author: micha
"""
from .genn_network import GennNetwork

class Network(object):
    """
    Manage the network in python.
    """
    pynn_populations = {}
    pynn_projections = {} 
    pynn_params = {}
    dt = 0.1
    
    def __init__(self, modelname, float_prec='float', nGPU=0, modelseed=0):
        """
        Parameters:
        modelname - the name of the model (string)
        float_prec - floating-point precision (double or float)
        nGPU - 0: run on CPU, 1: run on default GPU, n: run on GPU number 'n-2'.
        """
        self.modelname = modelname
        self.float_prec = float_prec
        self.modelseed = modelseed
        self.nGPU = nGPU

           
    def set_dt(self, dt):
        self.dt = dt

    def _set_simtime(self, simtime):
        raise(NotImplementedError)
    
    def generate_GeNN_code(self):
        """
        Initiates the translation from pyNN representation into the GeNN 
        representation.
        
        Returns the code for the GeNN model.
        """
        genn_network = GennNetwork(self)
        genn_network.translate_network_to_genn()
        modelcode = genn_network.generate_model_cc()
        return modelcode
    
    def _execute(self):
        raise(NotImplementedError)
    
    def add_pynn_population(self, population, label):
        """
        Add a pyNN.Population to the network.
        
        Parameters:
        population - the pyNN.Population object
        label - a unique label
        """
        if label in self.pynn_populations.keys():
            raise(Exception(
                "Population label {} is not unique.".format(label)))
        self.pynn_populations[label] = population
        
    def add_pynn_projection(self, projection, label):
        """
        Add a pyNN.Projection to the network.
        Parameters:
        projection - the pyNN.Projection object
        label - a unique label
        """
        if label in self.pynn_projections.keys():
            raise(Exception(
                'Projection label {} is not unique.'.format(label)))
        self.pynn_projections[label] = projection
    
    def add_pynn_recorder(self, recorder):
        """
        """
        pass
        
    def _add_pynn_params(self, parameters, label, param_seq, c_type):
        """
        Add a parameter set to the model name space, e.g. used by populations 
        or projections. 
        
        Parameters:
        parameters - the ParameterSpace object
        label - a unique label
        param_seq  -the required sequence of the parameters in the c code
        c_type - the C type of the parameter array
        """
        if label in self.pynn_params.keys():
            raise(Exception(
                'Parameter set label {} is not unique.'.format(label)))
        parameters['label'] = label
        parameters['param_seq'] = param_seq
        parameters['c_type'] = c_type
        self.pynn_params[label] = parameters
