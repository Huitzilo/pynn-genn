# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 11:00:30 2015

@author: micha

This file contains the templates that are needed to generate a runner.cc 
program. The resulting program will control the simulation of the network on 
GeNN.
"""

# I need:
# "mapper" definition (map_classol.h)
# "mapper" code (map_classol.cc, includes MBody1_CODE/runner.cc (generated))
# CUDA kernel code:
# sim.h (classol_sim.h, includes MBody1.cc (the model definition), and map_classol.cc)
# sim.cu (the actual kernel, contains main(), classol_sim.cu, includes classol_sim.h)

# so put everything in one large .cu file and be done with it.
# sequence:
# include *_CODE/runner.cc 
# network object definition definition (network object that contains the functionality, should also define "scalar")
# "mapper" code
# model definition
# main()

header = """
#include ${modelname}_runner.cc
"""


classdef = """
class PynnModel
{
  public:
    NNmodel model;
    PynnModel();
    ~PynnModel();
    void init();
    void run(scalar);
    void finalise();
$any_other_code
}
"""
# substitutions: 
# any_other_code 

constructor = """
PyNNModel::PyNNModel()
{
  modelDefinition(model);   // from GeNN
  allocate_mem();           // from GeNN
  initialize();             // from GeNN
$class_vars
}
"""
# subsitutions:
# class_vars - class variables that need initialising

init = """
PyNNModel::init()
{
  // set up neurons
  // set up synapses
  // set up recorders
}
"""

run = """
PyNNModel::run(scalar runtime):
{
  unsigned int steps = (int) (runtime/DT);
  for (int i = 0; i < runtime; i++) {
    stepTime${which}
  }
}
"""


footer = """
"""