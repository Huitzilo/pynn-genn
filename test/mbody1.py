# -*- coding: utf-8 -*-
"""
Created on Fri Dec  5 13:58:59 2014

@author: micha
"""

num_al = _NAL


import pyNN.genn as p

#?  model.setName("MBody1"); 

p.setup()

# Population constructor
# Population(size, cellclass, cellparams=None, structure=None, initial_values={}, label=None):
        
#  model.addNeuronPopulation("PN", _NAL, POISSONNEURON, myPOI_p, myPOI_ini);
pn = p.Population(num_al, 
                       p.PoissonNeuron, 
                       cellparams=mypoi_p, 
                       structure=None, 
                       initial_values=mypoi_ini, 
                       label="PN")


#  model.addNeuronPopulation("KC", _NMB, TRAUBMILES, stdTM_p, stdTM_ini);
kc = p.Population(num_kc, 
                  p.TraubMiles,
                  cellparams=stdtm_p,
                  structure=None,
                  initial_values=stdtm_ini,
                  label="KC")
                  
#  model.addNeuronPopulation("LHI", _NLHI, TRAUBMILES, stdTM_p, stdTM_ini);
lhi = p.Population(num_lhi,
                   p.TraubMiles,
                   cellparams=stdtm_p,
                   structure=None,
                   initial_values=stdtm_ini,
                   label="LHI")
                   
#  model.addNeuronPopulation("DN", _NLB, TRAUBMILES, stdTM_p, stdTM_ini);
dn = p.Population(num_lb,
                  p.TraubMiles,
                  cellparams=stdtm_p,
                  structure=None,
                  initial_values=stdtm_ini)


#    def __init__(self, presynaptic_neurons, postsynaptic_neurons, connector,
#                 synapse_type=None, source=None, receptor_type=None,
#                 space=Space(), label=None):

#  model.addSynapsePopulation("PNKC", NSYNAPSE, DENSE, INDIVIDUALG, NO_DELAY, EXPDECAY, "PN", "KC", myPNKC_p, postSynV,postExpPNKC);
# Some parameters are not addressed by standard PyNN Projection():
# DENSE, 
# INDIVIDUALG, 
# NO_DELAY 
# EXPDECAY 
# myPNKC_p, 
# postSynV,
# postExpPNKC

# DENSE, INDIVIDUALG, NO_DELAY will have to sorted out in the Connector code.
# it really depends on what set_weights() is doing. 
# Delay is not set in the constructor but only afterwards via set('delay').
# Implement delay at a later stage.
# How should we handle EXPDECAY?

prj_pnkc = p.Projection(pn, kc, 
                        p.AllToAllConnector(), 
                        synapse_type=p.NSynapse, 
                        label="PNKC")
                        
  model.addSynapsePopulation("PNLHI", NSYNAPSE, ALLTOALL, INDIVIDUALG, NO_DELAY, EXPDECAY, "PN", "LHI", myPNLHI_p, postSynV, postExpPNLHI);
  model.addSynapsePopulation("LHIKC", NGRADSYNAPSE, ALLTOALL, GLOBALG, NO_DELAY, EXPDECAY, "LHI", "KC", myLHIKC_p, postSynV, postExpLHIKC);
  model.setSynapseG("LHIKC", gLHIKC); # set('weight')
  model.addSynapsePopulation("KCDN", LEARN1SYNAPSE, ALLTOALL, INDIVIDUALG, NO_DELAY, EXPDECAY, "KC", "DN", myKCDN_p, postSynV, postExpKCDN);
  model.addSynapsePopulation("DNDN", NGRADSYNAPSE, ALLTOALL, GLOBALG, NO_DELAY, EXPDECAY, "DN", "DN", myDNDN_p, postSynV, postExpDNDN);
  model.setSynapseG("DNDN", gDNDN);