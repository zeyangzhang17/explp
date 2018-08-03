# Module: set 

# Functions:
    # set.objective()
    # set.multi_objective()
    # set.constraint()
    # set.integer_constraint()

    
    
# Last Updated: 3rd August 2018



import numpy as np
import pandas as pd
import copy


# Objective Function:

def objective(Objective_Name=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):
    
    global obj_names, obj_coef, variable_names, obj_max
    
    # check if the problem is multi-objective
    
    if len(Objective_Name) != 1:
        print('Error! Please Enter ONE and ONLY ONE Objective Name.\nFor Multi-Objective Problems, Please Use multi_objective() Function.\n')
    else:
        print('\n')
        
    len_var_name = len(Variable_Name)
    len_var_coef = len(Variable_Coefficient)

    len_counter = 0
    
    # check if the length of variable coefficients are matching with names

    for len_counter in range(len_var_coef):
        if len(Variable_Coefficient[len_counter]) != len_var_name:
            print('Error! The Length of Variable Name and Variable Coefficient DO NOT Match!')
            break
        else:
            len_counter += 1
    
    # Transforming to the stardard form
    
    if Maximise == True:
        obj_coef = Variable_Coefficient
    else:
        obj_coef = [- value for value in Variable_Coefficient]
    
    obj_names = Objective_Name 
    variable_names = Variable_Name
    obj_max = Maximise
    
    return obj_names, obj_coef, variable_names, obj_max



# Multi_objective Function:

def multi_objective(Objective_Name=[], Lambda=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):
    
    global multi_obj_names, obj_names, multi_obj_coef, obj_coef, variable_names, multi_obj_max
    
    # check if the problem is single objective
    
    if len(Objective_Name) <= 1:
        print('Error! Please Enter MORE THAN ONE Objective Name.\nFor Single-Objective Problems, Please Use objective() Function.\n')
    
    # check if the length of objective and Lambda are matching
    
    if len(Objective_Name) != len(Lambda):
        print('Error! The Length of Objective Name and Lambda DO NOT Match!\n')
    
    # check if Lambda is fit to weight criterion
    
    if sum(Lambda) != 1 or any(Lambda)<0:
        print('Error! Any Lambda must be non-negative and The sum of all Lambda must be 1!\n')
        
    # # check if the length of objective and variable coefficient are matching
    
    len_var_name = len(Variable_Name)
    len_var_coef = len(Variable_Coefficient)
    
    if len_var_coef != len(Objective_Name):
        print('Error! The Length of Objective Name and Variable Coefficient DO NOT Match!\n')

    # check if the Length of Variable Name and Variable Coefficient are matching 
        
    len_counter = 0

    for len_counter in range(len_var_coef):
        if len(Variable_Coefficient[len_counter]) != len_var_name:
            print('Error! The Length of Variable Name and Variable Coefficient DO NOT Match!')
            break
        else:
            len_counter += 1
    
    # transform objective coefficient into standard form
    
    if Maximise == True:
        multi_obj_coef = Variable_Coefficient
    else:
        multi_obj_coef = [[- value for value in thelist] for thelist in Variable_Coefficient]
    
    obj_coef = []
    weighted_obj_coef = []
    weight_counter = 0
    
    # compute weighted objective coefficient
    
    for weight_counter in range(len(Lambda)):
        weighted_obj_coef.append([Lambda[weight_counter] * value for value in multi_obj_coef[weight_counter]])
    
    DF_obj_coef = pd.DataFrame(data=weighted_obj_coef)    
    row_counter = 0
    
    for row_counter in range(len_var_name):
        obj_coef.append(sum(DF_obj_coef[row_counter]))
        row_counter += 1
    
    multi_obj_names = Objective_Name
    obj_names = ['Weighted Total Objective']
    variable_names = Variable_Name
    multi_obj_max = Maximise
    
    return multi_obj_names, obj_names, multi_obj_coef, obj_coef, variable_names, multi_obj_max



# Constraint Function:

def constraint(Constraint_Name=[], Constraint_Coefficient=[], Bound_Name=[], Bound_Value=[], Maximise=False, Type=[]):
    
    global constraint_names, constraint, bound_names, bound, constraint_type
    
    # check for the length of constraints name input
    
    len_con_name = len(Constraint_Name)
    len_con_coef = len(Constraint_Coefficient)
   
    # check if the length of constraints coefficients are matching with names
    
    len_counter = 0

    for len_counter in range(len_con_coef):
        if len(Constraint_Coefficient[len_counter]) != len_con_name:
            print('Error! The Length of Constraint Name and Constraint Coefficient DO NOT Match!')
            break
        else:
            len_counter += 1
    
    # Transforming to the stardard form
    
    if Maximise == False:
        constraint = Constraint_Coefficient
        bound = Bound_Value
    else:
        constraint = [- value for value in Constraint_Coefficient]
        bound = [- value for value in Bound_Value]  
    
    constraint_names = Constraint_Name
    bound_names = Bound_Name
    con_max = Maximise
    constraint_type = Type
    
    return constraint_names, constraint, bound_names, bound, constraint_type



# Integer_constraint Function:

def integer_constraint(Integer_Variable_Names = []):
    
    global Integer_Variable_Name, Integer_Index
    
    # check if the integer variable name is in the list of variables
    
    if set(Integer_Variable_Names).issubset(variable_names) == False:
        print('Error! The Integer Variable Name DOES NOT Match with Variable Name in Objectives')
    
    # compute the index of integer variables
    
    Integer_Index = []
    
    index_counter = 0
    
    for index_counter in range(len(Integer_Variable_Names)):
        Integer_Index.append(obj_names.index(Integer_Variable_Names[index_counter]))
        index_counter += 1
    
    Integer_Variable_Name = Integer_Variable_Names
    
    return Integer_Variable_Name, Integer_Index


        
# Before soving the problem, firstly record all the input with deep copy in case the variable changes in the following steps

global Deep_Copy_objective, Deep_Copy_multi_objective, Deep_Copy_constraint, Deep_Copy_integer_constraint

try:
    Deep_Copy_objective = copy.deepcopy([obj_names, obj_coef, variable_names, obj_max])
    Deep_Copy_multi_objective = copy.deepcopy([multi_obj_names, obj_names, multi_obj_coef, obj_coef, variable_names, multi_obj_max])
    Deep_Copy_constraint = copy.deepcopy([constraint_names, constraint, bound_names, bound, constraint_type])
    Deep_Copy_integer_constraint = copy.deepcopy([Integer_Variable_Name, Integer_Index])
except NameError:
    pass



# The End of Set Module
