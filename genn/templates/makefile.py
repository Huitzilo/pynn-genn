# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 20:37:58 2014

@author: micha
"""

# The makefile takes these substitutions (all strings):
# $modeldir  - the modeldir
# $gp - the GeNNPATH
# $timestamp - a date as a timestamp
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

ROOTDIR		:= $modeldir
EXECUTABLE	:= PyNNGeNN_model
SOURCES		:= PyNNGeNN_model.cu

include	$gp/userproject/include/makefile_common_gnu.mk

## $timestamp
"""




