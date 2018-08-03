# Module: alternative

# Functions:
    # alternative.objective()
    # alternative.multi_objective()
    # alternative.constraint()
    # alternative.integer_constraint()
    # alternative.compare()

    
# Last Updated: 3rd August 2018



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import math

import explp.set
from explp import solve
from explp import sensitivity_analysis


# Objective Function:

def objective(Objective_Name=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):
    
    explp.set.objective(Objective_Name, Objective_Name, Variable_Coefficient, Maximise)


# Multi_objective Function:

def multi_objective(Objective_Name=[], Lambda=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):

    explp.set.multi_objective(Objective_Name, Lambda, Variable_Name, Variable_Coefficient, Maximise)
    

# Constraint Function:

def constraint(Constraint_Name=[], Constraint_Coefficient=[], Bound_Name=[], Bound_Value=[], Maximise=False, Type=[]):

    explp.set.constraint(Constraint_Name, Constraint_Coefficient, Bound_Name, Bound_Value, Maximise, Type)

# Integer_constraint Function:

def integer_constraint(Integer_Variable_Names = []):
    
    explp.set.integer_constraint(Integer_Variable_Names)
    

# Compare Function:

def compare():
    
    # firstly retrieve the deep copy of original inputs and solutions
    
    
    


# The End of Alternative Module