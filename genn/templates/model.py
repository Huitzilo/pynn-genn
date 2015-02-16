# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 16:46:25 2014

@author: micha
"""

# model header, 2 substitutions
# $dt:  timestep in MS
# $timestamp: a time stamp
model_header = """
/* GeNN model generated by PyNN */
/* $timestamp */

#define DT $dt

#include "modelSpec.h"
#include "modelSpec.cc"

"""

# ... in between here we later insert the parameter definitions

# model_definition_header substitutes $modelname
model_definition_header = """
void modelDefinition(NNmodel &model) 
{
  initGeNN();
  model.setName("$modelname");
"""

# ... then come the NeuronPopulations

# ... then the SynapsePopulations

# ... then anything alse we'd like to add (e.g model.setSynapseG() or so)

model_GPU_selection = """
  model.setGPUDevice($nGPU);
"""

model_definition_footer = """
  model.setSeed($model_seed);
  model.setPrecision($C_TYPE);
}
"""