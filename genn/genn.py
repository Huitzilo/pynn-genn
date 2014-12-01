# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 14:22:20 2014

@author: micha
"""
from string import Template
import time
import os
from . import simulator
from .templates import model

class Network(object):
    """
    Manage the network in python.
    """
    param_defs = {}
    neuron_populations = {}
    synapse_populations = {}
    other_code = {}
    dt = 0.1
        
    def run(self, simtime):
        """
        compile the network if necessary and run the whole thing.
        """
        self._set_simtime(simtime)
        if simulator.state.needs_recompile:
            self._recompile()
        self._execute()

    def _set_simtime(self, simtime):
        pass
    
    def _recompile(self):
        pass
    
    def _execute(self):
        pass
    
    def set_dt(self, dt):
        self.dt = dt

    def add_param_def(self, paramdef):
        pdef_name = paramdef.code_params['name']
        self.param_defs[pdef_name] = paramdef.get_the_code()

    def add_neuron_population(self, neuronpop):
        npop_name = neuronpop.code_params['name']
        self.neuron_populations[npop_name] = neuronpop.get_the_code()

    def add_synapse_population(self, synapsepop):
        spop_name = synapsepop.code_params['name']
        self.synapse_populations[spop_name] = synapsepop.get_the_code()
        
    def generate_model_cc(self):
        """
        Generate the code according to the network specification.
        Returns a string that represents the .cc contents.
        """
        timestamp = time.asctime()
        header_t = Template(model.model_header)
        header = header_t.substitute(dt=self.dt, timestamp=timestamp)
        pdefs = '\n'.join(self.param_defs.values())
        mname = os.path.basename(simulator.state.modeldir)
        mdef_header_t = Template(model.model_definition_header)
        mdef_header = mdef_header_t.substitute(modelname=mname)
        npops = '\n'.join(self.neuron_populations.values())
        spops = '\n'.join(self.synapse_populations.values())        
        other = '\n'.join(self.other_code.values())
        code = '\n'.join(header, pdefs, mdef_header, npops, spops, other)
        return code
        
        
class ParamDef(object):
    """
    The python representation of a parameter definition.
    """
    param_header = "$c_type($name[$size]) = {"
    param_body = "$val /* $param_name */"
    param_footer = "};"

    def __init__(self, name, param_dict, param_seq, c_type='float'):
        """
        The GeNN representation of a parameter definition (a C array).
        
        Parameters:
        name: reference of the parameter array
        param_dict: dictionary of parameters
        param_seq: list of keys to the disctionary that define param sequence
        c_type: C type of the parameter dictionary
        """
        self.code_params = {
            "name" :name,
            "param_dict": param_dict,
            "param_seq": param_seq,
            "c_type": c_type}
        
    def get_the_code(self):
        """
        Generate the code.
        """
        header_template = Template(self.param_header)
        header_dict = {'c_type': self.code_params['c_type'],
                       'name': self.code_params['name'],
                       'size': len(self.code_params['param_dict'].keys())}
        header = header_template.substitute(header_dict)
        body_template = Template(self.param_body)
        bodyitems = []
        for pname in self.code_params['param_seq']:
            pval = self.code_params['param_dict'][pname]
            bodyitems.append(body_template.substitute(val=pval, 
                                                      param_name=pname))
        body = [",\n".join(bi) for bi in bodyitems]
        code = header + '\n' + body + '\n' + self.param_footer
        return code
        
     

class GeNNCode(object):
    """
    Parent class for Neuron and Synapse Populations.
    """
    def get_the_code(self):
        """
        Generate the code
        """
        code = Template(self.code_template)
        self.code = code.substitute(self.param_dict)
        return self.code

class NeuronPopulation(GeNNCode):
    """
    The python model of the GeNN NeuronPopulation.
    """
    code_template = "model.addNeuronPopulation(" +\
                    "\"$name\", " +\
                    "$n, " +\
                    "$neurontype, " +\
                    "$para, " +\
                    "$ini);"
    
    def __init__(self, name, n, neurontype, para, ini):
        """
        The GeNN representation of a neuron population.
        
        Parameters:
        name: identifier of the population (string)
        n: number of neurons in the population (int)
        neurontype: Type of the neurons (int)
        para: Parameters of this neuron type (pointer ref as string)
        ini: Initial values for variables of this neuron type (pointer ref as string)
        """
        self.param_dict = {
            "name": name,
            "n": n,
            "neurontype": neurontype,
            "para": para,
            "ini": ini}
            
        
class SynapsePopulation(GeNNCode):
    """
    The python model of the GeNN SynapsePopulation.
    """
    code_template = "model.addSynapsePopulation(" +\
                    "\"$name\", " +\
                    "$sType, " +\
                    "$sConn, " +\
                    "$gType, " +\
                    "$delaySteps, " +\
                    "$postsyn, " +\
                    "\"$prename\", " +\
                    "\"$postname\", " +\
                    "$sParam, " +\
                    "$postSynVParamsIni, " +\
                    "$postSynVParams);"    
                    
    def __init__(self, name, sType, sConn, gType, delaySteps, postsyn, prename, 
                 postname, sParam, postSynVParamsIni, postSynVParams):
        """
        The GeNN representation of a synapse Population.
        
        Parameters:
        
        name: The name of the synapse population (string)
        sType: The type of synapse to be added (int)
        sConn: The type of synaptic connectivity (int) 
        gType: The way how the synaptic conductivity g will be defined (int)
        delaySteps: Number of delay slots (int)
        postSyn: Postsynaptic integration method (int)
        preName: Name of the per-synaptic neuron population (string)
        postName: Name of the post-synaptic neuron population (string)
        sParam: pointer to array of floats that contains synapse parameter values (string)
        postSynVParamsIni: pointer to array of initial postsyn parameters (string)
        postSynVParams: pointer to array of postsyn parameters (string)
        """
        self.param_dict = {
            "name": name,
            "sType": sType, 
            "sConn": sConn, 
            "gType":gType, 
            "delaySteps": delaySteps, 
            "postsyn": postsyn, 
            "prename": prename, 
            "postname": postname, 
            "sParam": sParam, 
            "postSynVParamsIni": postSynVParamsIni, 
            "postSynVParams": postSynVParams}
                

      
