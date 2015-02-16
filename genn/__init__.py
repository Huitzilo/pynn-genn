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
from pyNN import common
from pyNN.common.control import DEFAULT_MAX_DELAY, DEFAULT_TIMESTEP, DEFAULT_MIN_DELAY
from pyNN.connectors import *
from pyNN.recording import *
from . import simulator
from .standardmodels import *
from .populations import Population, PopulationView, Assembly
from .projections import Projection
from .cells import *


logger = logging.getLogger("PyNN-GeNN")

def setup(timestep=DEFAULT_TIMESTEP, min_delay=DEFAULT_MIN_DELAY, 
          max_delay=DEFAULT_MAX_DELAY, **extra_params):
    # call superclass setup
    common.setup(timestep, min_delay, max_delay, **extra_params)
    # set up the basic functionality
    simulator.state.keep_dirs =  extra_params.get('keep_dirs', False)
    simulator.state.modelname = extra_params.get('modelname', 'GeNNmodel')
    simulator.state.float_prec = extra_params.get('float_prec', 'float')
    simulator.state.nGPU = extra_params.get('nGPU', 0)
    simulator.state.clear()
    
    
run, run_until = common.build_run(simulator)
run_for = run
