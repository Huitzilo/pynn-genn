# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 14:22:20 2014

@author: micha

Essentially a python wrapper for GeNN functionality.
"""
from string import Template
import time
import numpy
from .templates import model

class Network(object):
    """
    Manage the network in python.
    """
    pynn_populations = {}
    pynn_projections = {} 
    pynn_params = {}
    
    genn_param_defs = {}
    genn_neuron_populations = {}
    genn_synapse_populations = {}
    genn_other_code = {}
    dt = 0.1
    
    def __init__(self, modelname, float_prec='float', nGPU=0, modelseed=0):
        """
        Parameters:
        modelname - the name of the model (string)
        float_prec - floating-point precision (double or float)
        nGPU - 0: run on CPU, 1: run on default GPU, n: run on GPU number 'n-2'.
        """
        self.modelname = modelname
        self.float_prec = float_prec
        self.modelseed = modelseed
        self.nGPU = nGPU
        if self.nGPU > 1:
            nGPU_t = Template(model.model_GPU_selection)
            nGPU_code = nGPU_t.substitute(nGPU=self.nGPU-2)
            self.genn_other_code['GPUsel'] = nGPU_code
           
    def set_dt(self, dt):
        self.dt = dt

    def _set_simtime(self, simtime):
        raise(NotImplementedError)
    
    def _recompile(self):
        self._translate_network_to_genn()
        code = self._generate_model_cc()
        print code
        # call buildmodel.sh from GeNN distribution 
        # cd model && buildmodel.sh && make clean && make release
        raise(NotImplementedError)
    
    def _execute(self):
        raise(NotImplementedError)
    
    def add_pynn_population(self, population, label):
        """
        Add a pyNN.Population to the network.
        
        Parameters:
        population - the pyNN.Population object
        label - a unique label
        """
        if label in self.pynn_populations.keys():
            raise(Exception(
                "Population label {} is not unique.".format(label)))
        self.pynn_populations[label] = population
        
    def add_pynn_projection(self, projection, label):
        """
        Add a pyNN.Projection to the network.
        Parameters:
        projection - the pyNN.Projection object
        label - a unique label
        """
        if label in self.pynn_projections.keys():
            raise(Exception(
                'Projection label {} is not unique.'.format(label)))
        self.pynn_projections[label] = projection
        
    def _add_pynn_params(self, parameters, label, param_seq, c_type):
        """
        Add a parameter set to the model name space, e.g. used by populations 
        or projections. 
        
        Parameters:
        parameters - the ParameterSpace object
        label - a unique label
        param_seq  -the required sequence of the parameters in the c code
        c_type - the C type of the parameter array
        """
        if label in self.pynn_params.keys():
            raise(Exception(
                'Parameter set label {} is not unique.'.format(label)))
        parameters['label'] = label
        parameters['param_seq'] = param_seq
        parameters['c_type'] = c_type
        self.pynn_params[label] = parameters
        
    def _add_param_def(self, paramdef):
        """
        Adds a ParamDef() parameter definition to the model.
        This definition will be referenced in the code by its name as specified 
        in ParamDef(name=name,...).
        """
        pdef_name = paramdef.code_params['name']
        self.genn_param_defs[pdef_name] = paramdef.get_the_code()

    def _add_neuron_population(self, neuronpop):
        """
        Add a NeuronPopulation to the model.
        """
        npop_name = neuronpop.code_params['name']
        self.genn_neuron_populations[npop_name] = neuronpop.get_the_code()

    def _add_synapse_population(self, synapsepop):
        """
        Add a SynapsePopulation to the model.
        """
        spop_name = synapsepop.code_params['name']
        self.genn_synapse_populations[spop_name] = synapsepop.get_the_code()
    
    def _check_unique_parameters(self, parameters):
            """
            We're currently only supporting Populations with all neurons having 
            the same parameters. This function checks whether the parameter 
            space fulfils this criterion and returns the one-d parameter space,
            or raises NotImplementedError instead.
            """
            retparm = {}
            for k in parameters.keys():
                param_val = numpy.unique(parameters[k])
                if len(param_val) > 1:
                    error = "Population parameters are not homogeneous. " + \
                    "Currently, we only support Populations in which all " + \
                    "neurons have the same parameters."
                    raise(NotImplementedError(error))
                else:
                    retparm[k] = param_val[0]
            return retparm

    def _translate_network_to_genn(self):
        """
        Collects all the pyNN components (Parameters, Populations, Projections, 
        Recorders) and translates them into their genn counterparts.
        """
        for pop in self.pynn_populations.values():
            genn_pop = NeuronPopulation(
                            name=pop.label,
                            n=len(pop.all_cells),
                            neurontype=pop.celltype.__class__.__name__)
            self._add_neuron_population(genn_pop)
            pop_params = self._check_unique_parameters(pop._parameters)
            pop_params = ParamDef(name="{}_params".format(pop.label),
                                  param_dict=pop_params,
                                  param_seq=pop.celltype.param_seq,
                                  c_type=self.float_prec) 
            self._add_param_def(pop_params)
            for k in pop.initial_values.keys():
                pop.initial_values[k].shape = pop.size
                pop.initial_values[k] = pop.initial_values[k].evaluate()
            pop_ini_params = self._check_unique_parameters(pop.initial_values)
            pop_ini_params = ParamDef(name="{}_ini_params".format(pop.label),
                                      param_dict=pop_ini_params,
                                      param_seq=pop.celltype.ini_seq,
                                      c_type=self.float_prec)
            self._add_param_def(pop_ini_params)
        for prj in self.pynn_projections.values():
            self._add_synapse_population(prj)
        for pd in self.pynn_params.values():
            genn_pd = ParamDef(name=pd['label'], 
                               param_dict=pd, 
                               param_seq=pd['param_seq'],
                               c_type=pd['c_type'])
            self._add_param_def(genn_pd)
    
    def _generate_model_cc(self):
        """
        Generate the code according to the network specification.
        Returns a string that represents the .cc contents.
        """
        timestamp = time.asctime()
        header_t = Template(model.model_header)
        header = header_t.substitute(dt=self.dt, timestamp=timestamp)
        pdefs = '\n'.join(self.genn_param_defs.values())
        mdef_header_t = Template(model.model_definition_header)
        mdef_header = mdef_header_t.substitute(modelname=self.modelname)
        npops = '\n'.join(self.genn_neuron_populations.values())
        spops = '\n'.join(self.genn_synapse_populations.values())        
        other = '\n'.join(self.genn_other_code.values())
        mdef_footer_t = Template(model.model_definition_footer)
        mdef_footer = mdef_footer_t.substitute(model_seed=self.modelseed,
                                               C_TYPE=self.float_prec.upper())
                                               
        code = '\n'.join([header, 
                          "  // PARAMETER DEFINITIONS #####################", 
                          pdefs, 
                          mdef_header, 
                          "  // NEURON POPULATIONS ########################",
                          npops, 
                          "\n  // SYNAPSE POPULATIONS / PROJECTIONS ########",
                          spops, 
                          "\n  // OTHER CODE ###############################",
                          other,
                          mdef_footer])
        return code


        

class ParamDef(object):
    """
    The python representation of a parameter definition.
    """
    param_header = "$c_type($name[$size]) = {"
    param_body = "  $val  \t/* $param_name */"
    param_footer = "};"

    def __init__(self, name, param_dict, param_seq, c_type='float'):
        """
        The GeNN representation of a parameter definition (a C array).
        
        Parameters:
        name: reference of the parameter array (must be unique)
        param_dict: dictionary of parameters
        param_seq: list of keys to the dictionary that define param sequence
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
                       'size': len(self.code_params['param_seq'])}
        header = header_template.substitute(header_dict)
        body_template = Template(self.param_body)
        bodyitems = []
        for pname in self.code_params['param_seq']:
            pval = self.code_params['param_dict'][pname]
            bodyitems.append(body_template.substitute(val=pval, 
                                                      param_name=pname))
        body = ",\n".join(bodyitems) 
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
        self.code = code.substitute(self.code_params)
        return self.code

class NeuronPopulation(GeNNCode):
    """
    The python model of the GeNN NeuronPopulation.
    """
    code_template = "  model.addNeuronPopulation(" +\
                    "\"$name\", " +\
                    "$n, " +\
                    "$neurontype, " +\
                    "$para, " +\
                    "$ini);"
    
    def __init__(self, name, n, neurontype):
        """
        The GeNN representation of a neuron population.
        
        Parameters:
        name: identifier of the population (string) (must be unique)
        n: number of neurons in the population (int)
        neurontype: Type of the neurons (int)
        para: Parameters of this neuron type (pointer ref as string)
        ini: Initial values for variables of this neuron type (pointer ref as string)
        """
        self.code_params = {
            "name": name,
            "n": n,
            "neurontype": neurontype,
            "para": "{}_params".format(name),
            "ini": "{}_ini_params".format(name)}
            
        
class SynapsePopulation(GeNNCode):
    """
    The python model of the GeNN SynapsePopulation.
    """
    code_template = "  model.addSynapsePopulation(" +\
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
        
        name: The name of the synapse population (string) (must be unique)
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
        self.code_params = {
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
                

      
