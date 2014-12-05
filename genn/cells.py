# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 18:56:43 2014

@author: micha
"""

# These are defined in $GeNNPATH/lib/utils.h and extra_neurons.h

class GeNNNeuron(object):
    """
    Base class for GeNN Neurons.
    """
    def __init__(self, cell_params, initial_params):
        pass
    
class RulkovMapNeuron(object):
    """
    Rulkov map-based neurons.
    """
    pass

class PoissonNeurons(object):
    """
    Poisson process spike train generator.
    """
    pass

class TraubMiles(object):
    """
    Traub and Miles Hodgin-Huxley neurons.
    """
    pass

class Izhikevich(object):
    """
    Izhikevich neurons.
    """
    pass

class IzhikevichVar(object):
    """
    Izhikevich neurons with variable parameters.
    """
    pass

# from extra_neurons.h

class LeakyIF(object):
    """
    Leaky Integrate-And-Fire neurons.
    """
    pass

class RegularSpiking(object):
    """
    A regularly spiking neuron.
    """
    pass

class LeakyIntegrate(object):
    """
    Leaky Integrate and Fire number two.
    """
    pass

