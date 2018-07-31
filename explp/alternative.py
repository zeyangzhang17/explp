# Module: alternative

# Functions:
    # alternative.objective()
    # alternative.multi_objective()
    # alternative.constraint()
    # alternative.integer_constraint()
    # alternative.compare()

    
# Last Updated: 31st July 2018



import numpy as np
import pandas as pd
from explp import solve
from explp import sensitivity_analysis


# Objective Function:

def objective(Objective_Name=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):



# Multi_objective Function:

def multi_objective(Objective_Name=[], Lambda=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):



# Constraint Function:

def constraint(Constraint_Name=[], Constraint_Coefficient=[], Bound_Name=[], Bound_Value=[], Maximise=False, Type=[]):



# Integer_constraint Function:

def integer_constraint(Integer_Variable_Names = []):
    
    

# Compare Function:

def compare():
    


# The End of Alternative Module