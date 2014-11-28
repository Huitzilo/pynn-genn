# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 20:37:58 2014

@author: micha
"""

# The makefile takes these substitutions:
# 0 the modeldir
# 1 the GeNNPATH
# 2 a date as a timestamp
makefile = """
##--------------------------------------------------------------------------
##   Author: Thomas Nowotny
##  
##   Institute: Center for Computational Neuroscience and Robotics
##              University of Sussex
##            Falmer, Brighton BN1 9QJ, UK 
##  
##   email to:  T.Nowotny@sussex.ac.uk
##  
##   initial version: 2010-02-07
##  
##--------------------------------------------------------------------------

ROOTDIR		:= {0}
EXECUTABLE	:= PyNNGeNN_model
SOURCES		:= PyNNGeNN_model.cu

INCLUDE_FLAGS	:= 
LINK_FLAGS	:= 
CCFLAGS		:= 
NVCCFLAGS	:= 

ifdef COMSPEC
	include	{1}/lib/include/makefile_common_cygwin.mk
else
	include	{1}/lib/include/makefile_common.mk
endif

## {2}
"""
