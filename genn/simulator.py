# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 20:06:42 2014

@author: micha


"""

import logging
import os
import tempfile
import time
import subprocess
from string import Template

from pyNN import common
from .templates.makefile import makefile
from .nittygritty.pynn_network import Network

logging.basicConfig()
name = "PyNN-GeNN"
logger = logging.getLogger(name)
logger.setLevel(logging.INFO)

class ID(int, common.IDMixin):
    def __init__(self, n):
        """Create an ID object with numerical value `n`."""
        int.__init__(n)
        common.IDMixin.__init__(self)

class State(common.control.BaseState):
    """
    The State class essentially controls a temporary directory, in which the 
    generated C-Code is saved and compiled, and where any output from the 
    simulation is stored.
    
    State.clear() should be called after instratiation to obtain a fully
    initialised object. 
    """
    
    #these are indicators for the necessity of recompilation
    neuron_populations_changed = False
    synapse_populations_changed = False
    
    def __init__(self):
        common.control.BaseState.__init__(self)
        # check if GeNNPATH is set
        try:
           self.gp = os.environ['GENN_PATH']
        except KeyError, e:
            raise(Exception("GENN_PATH environment variable not set." + '\n' 
                    + "Please make it point to your GeNN installation." + '\n' 
                    + "Get GeNN from https://github.com/genn-team/genn ."))
        self.mpi_rank = 0
        self.num_processes = 1
        self.modeldir = None
        self.keep_dirs = False
        self.needs_recompile = True
        self.t = 0.
        self.simtime = 0.
        self.dt = 0.1
        self.id_counter = 0
        self.network = None
        self.modelname = None
        self.float_prec = None
        self.nGPU = 0
        
    def __del__(self):
        """
        Destructor. Make reasonably sure no files linger around when 
        interpreter exits (unless self.keep_dirs is set).
        """ 
        self._wipe_modeldir()
    
    def run_until(self, simtime):
        self._set_simtime(simtime)
        if self._check_for_recompile():
            self._create_modeldef_file()
            buildmodel_path = os.path.join(self.gp, 
                                           'lib', 
                                           'bin',
                                           'buildmodel.sh')
            subprocess.check_call([buildmodel_path, 'PyNNGeNN_model'], cwd=self.modeldir)
            subprocess.check_call(['make', 'clean'], cwd=self.modeldir)
            subprocess.check_call(['make', 'release'], cwd=self.modeldir)
        self.network._execute()

    def _check_for_recompile(self):
        logging.warn("Recompilation checks not yet implemented. " +
        "Defaulting to always recompiling.")
        return True

    def _set_simtime(self, simtime):
        self.simtime = simtime
        
    def clear(self):
        """
        Clears the modeldir, deletes the python representation of the GeNN 
        network, and resets the simulator.
        """
        # wipe the modeldir and make a new one
        self._wipe_modeldir()
        self._create_modeldir()
        # create a new makefile
        self._create_makefile()
        #do the rest...
        self.network = Network(
                time.strftime('{}_%y%m%d%H%M%S'.format(self.modelname)),
                float_prec=self.float_prec,
                nGPU=self.nGPU)
        self.reset()
        
    def reset(self):
        """Reset the state of the current network to time t = 0."""
        self.t_start = 0
        
    def _wipe_modeldir(self):
        """
        Removes any files from the temporary modeldir and deletes the dir 
        (if not disabled by setting self.keep_dirs.
        """
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
        mkf_t = Template(makefile)
        mkfstring = mkf_t.substitute(modeldir=self.modeldir, 
                                     gp=self.gp, 
                                     timestamp=time.asctime())
        with open(os.path.join(self.modeldir, 'Makefile'), 'w') as f:
            f.write(mkfstring)
            
    def _create_modeldef_file(self):
        modeldef_code = self.network.generate_GeNN_code()
        modeldef_path = os.path.join(self.modeldir, 'PyNNGeNN_model.cc')
        modeldef_file = open(modeldef_path, 'w')
        modeldef_file.write(modeldef_code)
        modeldef_file.close()

state = State()
