# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 14:59:38 2015

@author: micha
"""


import pyNN.genn as p

p.setup(nGPU=3, float_prec='double')

initial_params = {'V':-60., 'seed':12341234, 'SpikeTime':-10.} #should be default

poissons = p.Population(10, 
                        p.PoissonNeurons(), 
                        initial_values=initial_params,
                        label='poissons')
                        
poissons.set(rate=100., t_refrac=2., V_spike=20., V_rest=-60.)

poissons.record('spikes')

p.run(10000.)

data = poissons.get_data()

print(data)