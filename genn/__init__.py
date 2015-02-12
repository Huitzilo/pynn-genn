"""
The PyNN interface to GeNN.

Author: 
Michael Schmuker
School of Engineering and Informatics
University of Sussex
Brighton BN1 9QJ
UK 

General outline:

This module accepts a pyNN definition of a network, converts it to the 
corresponding GeNN definition (C-code), compiles it using the GeNN framework,
runs the compiled binary, and reads back the results. 


"""

import logging

logging.basicConfig()

import os
from pyNN import common, space
from pyNN.common.control import DEFAULT_MAX_DELAY, DEFAULT_TIMESTEP, DEFAULT_MIN_DELAY
from pyNN.connectors import *
from . import simulator
from .cells import *
from .populations import Population


def setup(timestep=DEFAULT_TIMESTEP, min_delay=DEFAULT_MIN_DELAY, 
          max_delay=DEFAULT_MAX_DELAY, **extra_params):
    # call superclass setup
    common.setup(timestep, min_delay, max_delay, **extra_params)
    # set up the basic functionality
    simulator.state.keep_dirs =  extra_params.get('keep_dirs', False)
    simulator.state.clear()
    
    
    