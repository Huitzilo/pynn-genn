"""
The PyNN interface to GeNN.

Author: 
Michael Schmuker
School of Engineering and Informatics
University of Sussex
Brighton 
UK 
"""

import logging

logging.basicConfig()

import os
from pyNN import common, space
from pyNN.common.control import DEFAULT_MAX_DELAY, DEFAULT_TIMESTEP, DEFAULT_MIN_DELAY
from pyNN.connectors import *
from . import simulator
from .cells import *


def setup(timestep=DEFAULT_TIMESTEP, min_delay=DEFAULT_MIN_DELAY, 
          max_delay=DEFAULT_MAX_DELAY, **extra_params):
    common.setup(timestep, min_delay, max_delay, **extra_params)
    simulator.state.keep_dirs =  extra_params.get('keep_dirs', False)
    simulator.state.clear()
    
    
    