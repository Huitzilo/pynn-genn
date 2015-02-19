# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 10:57:12 2015

@author: micha
"""

kernel_header = """
using namespace std;
#include "utils.h"
#include <cuda_runtime.h>

#include "PyNNGeNN_model.cc"

#include "mapper.cc"



"""

#TODO: run the model
main = """
int main(int argc, char* argv[])
{
  pynngenn model;

  
}
"""