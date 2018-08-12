# Module: alternative

# Functions:
    # alternative.objective()
    # alternative.multi_objective()
    # alternative.constraint()
    # alternative.integer_constraint()
    # alternative.compare()
    # alternative.new_input_checker()

    
# Last Updated: 8th August 2018



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
        explp.set.objective(Objective_Name, Variable_Name, Variable_Coefficient, Maximise)
        
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
        explp.set.multi_objective(Objective_Name, Lambda, Variable_Name, Variable_Coefficient, Maximise)
    
    multi_counter = 0
    print_counter = 0
        
    for multi_counter in range(len(multi_obj_names)):
        print("\nYou have now set the objective " + str(multi_obj_names[multi_counter]) + " to:\n")
        if multi_obj_max[multi_counter] == True:
            print("To Maximise " + str(obj_names[multi_counter]) + " = ", end="")
        else:
            print("To Minimise " + str(obj_names[multi_counter]) + " = ", end="")

        for print_counter in range(len(variable_names)-1):
            print(str(multi_obj_coef[multi_counter][print_counter]) + " * " + str(variable_names[print_counter]) + " + ", end = "")
            print_counter += 1
        print(str(multi_obj_coef[multi_counter][-1]) + " * " + str(variable_names[-1]) + " ; \n")  
        multi_counter += 1
        
    print("\nBy applying coefficients to multi-objectives, the problem is converted to single-objective: " + str(multi_obj_names) + " to: \n")
    print("To Maximise " + str(obj_names[0]) + " = ", end="")
              
    print_counter = 0
        
    for print_counter in range(len(variable_names)-1):
        print(str(obj_coef[print_counter]) + " * " + str(variable_names[print_counter]) + " + ", end = "")
        print_counter += 1
    print(str(obj_coef[-1]) + " * " + str(variable_names[-1]) + " ; \n")
    

# Constraint Function:

def constraint(Constraint_Name=[], Constraint_Coefficient=[], Bound_Name=[], Bound_Value=[], Maximise=False, Type=[]):
    
    try:   
        Original_constraint = copy.deepcopy(Deep_Copy_constraint)
        
        explp.set.constraint(Constraint_Name, Constraint_Coefficient, Bound_Name, Bound_Value, Maximise, Type)
        
        new_constraint = [constraint_names, constraint, bound_names, bound, constraint_type]
        constraint_name_list = ["The name of constraints", "The coefficient of constraints", "The name of the bound", "The value of the bound", "The constraints are less or equal to the bound", "The type of constraints"]
        new_input_checker(Original_constraint, new_constraint, constraint_name_list)
        
    except NameError:
        print("Previously the non-integer constraints are not defined.\n")
        explp.set.constraint(Constraint_Name, Constraint_Coefficient, Bound_Name, Bound_Value, Maximise, Type)
        
    print("\nNow the problem is subject to: \n")
              
    print_counter = 0
    var_counter = 0
        
    for print_counter in range(len(constraint_names)):
        print(str(constraint_type[print_counter]) + " constraints: " + str(constraint_names[print_counter]) + " : ", end = "")
        for var_counter in range(len(variable_names)-1):
            print(str(constraint[print_counter][var_counter]) + " * " + str(variable_names[var_counter]) + " + ", end = "")
            var_counter += 1
        print(str(constraint[print_counter][-1]) + " * " + str(variable_names[-1]) + " <= " + str(bound[print_counter]) + " ; \n")
        print_counter += 1 
        

# Integer_constraint Function:

def integer_constraint(Integer_Variable_Names = []):
    
    try: 
        Original_integer_constraint = copy.deepcopy(Deep_Copy_integer_constraint)
        
        explp.set.integer_constraint(Integer_Variable_Names)
        
        new_integer_constraint = [Integer_Variable_Name, Integer_Index]
        integer_constraint_name_list = ["The name of the variable set to integer", "The n-th variable in variable list is set to integer"]
        new_input_checker(Original_integer_constraint, new_integer_constraint, integer_constraint_name_list)
    
    except NameError:
        print("Previously the integer constraints are not defined.\n")
        explp.set.integer_constraint(Integer_Variable_Names)
        
        print("\nYou have now set the variables: " + str(Integer_Variable_Name[:]) + " to take only integer values.\n")
        

# Compare Function:

def compare():
    
    # firstly retrieve the deep copy of original solutions, and deep copy them in case changes 
    
    # try simplex
    
    original_objective_value_optimal = None
    
    try:
        Original_optimal_solution_Simplex = copy.deepcopy(Deep_Copy_Simplex)          
    except NameError:
        pass
    else:
        output_counter = 0
            
        print('\nThe previous optimal solution is as follows:\n')
        print('The optimal value for the objective is ' + str(Original_optimal_solution_Simplex[0]) + ' ;\n')
        original_objective_value_optimal = Original_optimal_solution_Simplex[0]
        
        try:
            original_variable_names = Deep_Copy_objective[2]
        except NameError:
            try:
                original_variable_names = Deep_Copy_multi_objective[4]
            except NameError:
                pass
            else:
                print('\nWhen: \n')    
                for output_counter in range(len(original_variable_names)):
                    print(str(original_variable_names[output_counter]) + ' is set to ' + str(Original_optimal_solution_Simplex[1][output_counter]) + '\n')
                    output_counter += 1
        else:
            print('\nWhen: \n')    
            for output_counter in range(len(original_variable_names)):
                print(str(original_variable_names[output_counter]) + ' is set to ' + str(Original_optimal_solution_Simplex[1][output_counter]) + '\n')
                output_counter += 1
    
    # try if no feasible solutions
    
    try:
        Original_NoFeasibleSolution = copy.deepcopy(Deep_Copy_NoFeasibleSolution)
        if Original_NoFeasibleSolution == True:
            print("\nThere are no feasible solutions for the problem under previous settings.\n")
            original_objective_value_optimal = None
    except NameError: 
        pass
    
    # try branch & bound
    
    try:
        Original_optimal_solution_Branch_and_Bound = copy.deepcopy(Deep_Copy_Branch_and_Bound)
    except NameError:
        pass
    else:
        output_counter = 0
            
        print('\nThe previous optimal solution is as follows:\n')
        print('The optimal value for the objective is ' + str(Original_optimal_solution_Branch_and_Bound[0]) + ' ;\n')
        original_objective_value_optimal = Original_optimal_solution_Branch_and_Bound[0]
        
        try:
            original_variable_names = Deep_Copy_objective[2]
        except NameError:
            try:
                original_variable_names = Deep_Copy_multi_objective[4]
            except NameError:
                pass
            else:
                print('\nWhen: \n')    
                for output_counter in range(len(original_variable_names)):
                    print(str(original_variable_names[output_counter]) + ' is set to ' + str(Original_optimal_solution_Branch_and_Bound[1][output_counter]) + '\n')
                    output_counter += 1
        else:
            print('\nWhen: \n')    
            for output_counter in range(len(original_variable_names)):
                print(str(original_variable_names[output_counter]) + ' is set to ' + str(Original_optimal_solution_Branch_and_Bound[1][output_counter]) + '\n')
                output_counter += 1
        
    
    # then solve and do sensitivity analysis under the new settings
    
    print('\n==================================================\n')
    print('The solution and sensitivity analysis under the new settings are as follows: ')
    print('\n==================================================\n')
    
    Solve()
    
    try:
        new_objective_value_optimal = optimal_solution_Simplex[0]
    except NameError:
        try:
            new_objective_value_optimal = optimal_solution_Branch_and_Bound[0]
        except NameError:
            new_objective_value_optimal = None
    
    Sensitivity_Analysis()
    
    print('\n==================================================\n')
    print('In conclusion, the optimal objective value has ', end = '')
    
    if original_objective_value_optimal == None:
        if new_objective_value_optimal == None:
            print('not changed.\nThe problem remains infeasible without optimal solution.\n')
        else:
            print('become feasible.\nThe problem now has an optimal solution, with objective value = ' + str(new_objective_value_optimal) + '.\n')
    
    else:
        if new_objective_value_optimal == None:
            print('become infeasible.\nThe problem now is infeasible without optimal solution.\n')
        elif original_objective_value_optimal > new_objective_value_optimal:
            print('changed.\nThe new objective value is smaller than the previous solution.\n')
        elif original_objective_value_optimal < new_objective_value_optimal:
            print('changed.\nThe new objective value is larger than the previous solution.\n')
        else:
            print('not changed.\nThe optimal objective value remains to be ' + str(original_objective_value_optimal) + ' .\n')
    
    print('\n==================================================\n')


    
# The End of Alternative Module
