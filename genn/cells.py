# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 18:56:43 2014

@author: micha
"""

from pyNN.models import BaseCellType

# These are defined in $GeNNPATH/lib/utils.h and extra_neurons.h

class RulkovMapNeuron(BaseCellType):
    """
    Rulkov map-based neurons.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class PoissonNeurons(BaseCellType):
    """
    Poisson process spike train generator.
    """
    recordable = ['spikes']
    default_parameters = {'rate': 0.1,      # 0 - firing rate
                          't_refrac': 2.5,  # 1 - seed
                          'V_spike': 20.,   # 2 - SpikeTime
                          'V_rest': -60.}
                          
    default_initial_values = {'V': 0.,              # 0 - V
                              'seed': 1234567,      # 1 - seed
                              'SpikeTime': -10.}    # 2 - SpikeTime

    parameter_checks = {}

class TraubMiles(BaseCellType):
    """
    Traub and Miles Hodgin-Huxley neurons.
    """
    default_parameters = {'gNa': 7.15,  # 0 - gNa: Na conductance in 1/(mOhms * cm^2)
                          'ENa': 50.,   # 1 - ENa: Na equi potential in mV
                          'gK': 1.43,   # 2 - gK: K conductance in 1/(mOhms * cm^2)
                          'EK': -95.,   # 3 - EK: K equi potential in mV
                          'gl': 0.02672,# 4 - gl: leak conductance in 1/(mOhms * cm^2)
                          'El': -63.563,# 5 - El: leak equi potential in mV
                          'Cmem':0.143} # 6 - Cmem: membr. capacity density in muF/cm^2
    default_initial_values = {'E':0.,               # 0 - membrane potential E
                              'p_Na_m': 0.529324,   # 1 - prob. for Na channel activation m
                              'p_Na_h': 0.3176767,  # 2 - prob. for not Na channel blocking h
                              'p_K_n': 0.5961207}   # 3 - prob. for K channel activation n
    parameter_checks = {}

class Izhikevich(BaseCellType):
    """
    Izhikevich neurons.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class IzhikevichVar(BaseCellType):
    """
    Izhikevich neurons with variable parameters.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

# from extra_neurons.h

class LeakyIF(BaseCellType):
    """
    Leaky Integrate-And-Fire neurons.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class RegularSpiking(BaseCellType):
    """
    A regularly spiking neuron.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class LeakyIntegrate(BaseCellType):
    """
    Leaky Integrate and Fire number two.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

