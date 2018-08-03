# Module: alternative

# Functions:
    # alternative.objective()
    # alternative.multi_objective()
    # alternative.constraint()
    # alternative.integer_constraint()
    # alternative.compare()
    # alternative.new_input_checker()

    
# Last Updated: 3rd August 2018



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import math

import explp.set
from explp import solve
from explp import sensitivity_analysis



# define a checker for outputing changes

def new_input_checker(original, new, name_list):
    
    # require the original, new, and name_list have the same length
    
    counter = 0
    
    for counter in range(len(original)):
        if original[counter] == new[counter]:
            print(str(name_list[counter]) + " have NOT been changed.\n")
        else:
            print(str(name_list[counter]) + " have been changed from " + str(original[counter]) + " to " + str(new[counter]) + "!\n")
        
        counter += 1
        

# Objective Function:

def objective(Objective_Name=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):
    
    try:
        Original_objective = copy.deepcopy(Deep_Copy_objective)
    
        explp.set.objective(Objective_Name, Variable_Name, Variable_Coefficient, Maximise)

        new_objective = [obj_names, obj_coef, variable_names, obj_max]
        objective_name_list = ["The name of the objective", "The coefficients of objective variable", "The name of variables", "The aim of maximising the objective"]
        new_input_checker(Original_objective, new_objective, objective_name_list)
        
    except NameError: 
        print("Previously the single objective is not defined.\n")
        
    print("Now the objective is set to: \n")
    
    print_counter = 0
        
    if obj_max == True:
        print("To Maximise " + str(obj_names[0]) + " = ", end="")
    else:
        print("To Minimise " + str(obj_names[0]) + " = ", end="")
            
    for print_counter in range(len(variable_names)-1):
        print(str(obj_coef[print_counter]) + " * " + str(variable_names[print_counter]) + " + ", end = "")
        print_counter += 1
    print(str(obj_coef[-1]) + " * " + str(variable_names[-1]) + " ; \n")
    

# Multi_objective Function:

def multi_objective(Objective_Name=[], Lambda=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):
    
    try:
        Original_multi_objective = copy.deepcopy(Deep_Copy_multi_objective)
        
        explp.set.multi_objective(Objective_Name, Lambda, Variable_Name, Variable_Coefficient, Maximise)
        
        new_multi_objective = [multi_obj_names, obj_names, multi_obj_coef, obj_coef, variable_names, multi_obj_max]
        multi_objective_name_list = ["The name of multiple objectives", "The name of integrated single objective", "The coefficients of multiple objectives variable", "The coefficients of single objective variable", "The name of variables", "The aim of maximising the multiple objective"]
        new_input_checker(Original_multi_objective, new_multi_objective, multi_objective_name_list)
        
    except NameError:
        print("Previously the multi-objectives are not defined.\n")
        
    
    

# Constraint Function:

def constraint(Constraint_Name=[], Constraint_Coefficient=[], Bound_Name=[], Bound_Value=[], Maximise=False, Type=[]):

    explp.set.constraint(Constraint_Name, Constraint_Coefficient, Bound_Name, Bound_Value, Maximise, Type)

# Integer_constraint Function:

def integer_constraint(Integer_Variable_Names = []):
    
    explp.set.integer_constraint(Integer_Variable_Names)
    

# Compare Function:

def compare():
    
    # firstly retrieve the deep copy of original inputs and solutions, and deep copy them in case changes 
    
    

    
    try:   
        Original_constraint = copy.deepcopy(Deep_Copy_constraint)
    except NameError:
        Original_constraint = None
        
    try: 
        Original_integer_constraint = copy.deepcopy(Deep_Copy_integer_constraint)
    except NameError:   
        Original_integer_constraint = None
    
    try:
        Original_tableau = copy.deepcopy(Deep_Copy_tableau)
    except NameError:
        Original_tableau = None
        
    try:
        Original_optimal_solution_Simplex = copy.deepcopy(Deep_Copy_Simplex)
    except NameError:
        Original_optimal_solution_Simplex = None
        
    try:
        Original_NoFeasibleSolution = copy.deepcopy(Deep_Copy_NoFeasibleSolution)
    except NameError: 
        Original_NoFeasibleSolution = None
    
    try:
        Original_optimal_solution_Branch_and_Bound = copy.deepcopy(Deep_Copy_Branch_and_Bound)
    except NameError:
        Original_optimal_solution_Branch_and_Bound = None
        
    
    
    
    
    Solve()
    Sensitivity_Analysis()

    


# The End of Alternative Module
