# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 18:56:43 2014

@author: micha
"""

from pyNN.models import BaseModelType

# These are defined in $GeNNPATH/lib/utils.h and extra_neurons.h

class RulkovMapNeuron(BaseModelType):
    """
    Rulkov map-based neurons.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class PoissonNeurons(BaseModelType):
    """
    Poisson process spike train generator.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class TraubMiles(BaseModelType):
    """
    Traub and Miles Hodgin-Huxley neurons.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class Izhikevich(BaseModelType):
    """
    Izhikevich neurons.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class IzhikevichVar(BaseModelType):
    """
    Izhikevich neurons with variable parameters.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

# from extra_neurons.h

class LeakyIF(BaseModelType):
    """
    Leaky Integrate-And-Fire neurons.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class RegularSpiking(BaseModelType):
    """
    A regularly spiking neuron.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

class LeakyIntegrate(BaseModelType):
    """
    Leaky Integrate and Fire number two.
    """
    default_parameters = {}
    default_initial_values = {}
    parameter_checks = {}

