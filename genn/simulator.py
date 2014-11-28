# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 20:06:42 2014

@author: micha
"""

import logging
import os
import tempfile
import time

from pyNN import common
from .templates.makefile import makefile

name = "GeNN"
logger = logging.getLogger("PyNN")
logger.setLevel(logging.INFO)

class State(common.control.BaseState):
    
    def __init__(self):
        common.control.BaseState.__init__(self)
        # check if GeNNPATH is set
        try:
           self.gp = os.environ['GeNNPATH']
        except KeyError, e:
            raise(Exception("GeNNPATH environment variable not set." + '\n' 
                    + "Please make it point to your GeNN installation." + '\n' 
                    + "Get GeNN from https://github.com/genn-team/genn ."))
        self.mpi_rank = 0
        self.num_processes = 1
#        self.network = None
        self.modeldir = None
        self.keep_dirs = False
        self.clear()
        
    def __del__(self):
        self._wipe_modeldir()
    
#    def run(self, simtime):
#        self.running = True
#        self.network.run(simtime * ms)
#        
#    def run_until(self, tstop):
#        self.run(tstop - self.t)
        
    def clear(self):
        # wipe the modeldir and make a new one
        self._wipe_modeldir()
        self._create_modeldir()
        # create a new makefile
        self._create_makefile()
        #do the rest...
        self.recorders = set([])
        self.id_counter = 0
        self.segment_counter = -1
#        if self.network:
#            for item in self.network.groups + self.network._all_operations:
#                del item
#        self.network = brian.Network()
#        self.network.clock = brian.Clock()
        self.reset()
        
    def reset(self):
        """Reset the state of the current network to time t = 0."""
#        self.network.reinit()
        self.running = False
        self.t_start = 0
#        self.segment_counter += 1
#        for group in self.network.groups:
#            if hasattr(group, "initialize"):
#                logger.debug("Re-initalizing %s" % group)
#                group.initialize()
        
    def _wipe_modeldir(self):
        if not (self.modeldir is None) and not self.keep_dirs:
            files = os.listdir(self.modeldir)
            for f in files:
                os.remove(os.path.join(self.modeldir,f))
            os.removedirs(self.modeldir)
        
    def _create_modeldir(self):
        td = tempfile.mkdtemp(prefix="PyNNGeNN_")
        self.modeldir = td
        logger.info("created modeldir in {}.".format(self.modeldir))
        
    def _create_makefile(self):
        mkfstring = makefile.format(self.modeldir, self.gp, time.asctime())
        with open(os.path.join(self.modeldir, 'Makefile'), 'w') as f:
            f.write(mkfstring)
            
        
        
        
        
#    def _get_dt(self):
#        if self.network.clock is None:
#            raise Exception("Simulation timestep not yet set. Need to call setup()")
#        return float(self.network.clock.dt/ms)
#
#    def _set_dt(self, timestep):
#        logger.debug("Setting timestep to %s", timestep)
#        #if self.network.clock is None or timestep != self._get_dt():
#        #    self.network.clock = brian.Clock(dt=timestep*ms)
#        self.network.clock.dt = timestep * ms
#    dt = property(fget=_get_dt, fset=_set_dt)
#
#    @property
#    def t(self):
#        return float(self.network.clock.t/ms)
        
    
state = State()
