# Module: set 

# Functions:
    # set.objective()
    # set.multi_objective()
    # set.constraint()
    # set.integer_constraint()
    # set.complete()

    
    
# Last Updated: 9th August 2018



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
    
    # check if the length of variable coefficients are matching with names
    if len_var_name != len_var_name:
        print('Error! The Length of Variable Name and Variable Coefficient DO NOT Match!')
    
    # Transforming to the stardard form
    
    if Maximise == True:
        obj_coef = Variable_Coefficient
    else:
        obj_coef = [- value for value in Variable_Coefficient]
    
    obj_names = Objective_Name 
    variable_names = Variable_Name
    obj_max = Maximise



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
    


# Constraint Function:

def constraint(Constraint_Name=[], Constraint_Coefficient=[], Bound_Name=[], Bound_Value=[], Maximise=False, Type=[]):
    
    global constraint_names, constraint, bound_names, bound, constraint_type
    
    # check for the length of constraints name input
    
    len_con_name = len(Constraint_Name)
    len_con_coef = len(Constraint_Coefficient)
   
    # check if the length of constraints coefficients are matching with names
    
    if len_con_coef != len_con_name:
        print('Error! The Length of Constraint Name and Constraint Coefficient DO NOT Match!')
    
    # Transforming to the stardard form
    
    if Maximise == False:
        constraint = Constraint_Coefficient
        bound = Bound_Value
    else:
        constraint = []
        neg_counter = 0
        for neg_counter in range(len(Constraint_Coefficient)):
            constraint.append([- value for value in Constraint_Coefficient[neg_counter]])
            neg_counter += 1
        bound = [- value for value in Bound_Value]  
    
    constraint_names = Constraint_Name
    bound_names = Bound_Name
    con_max = Maximise
    constraint_type = Type

    

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
        Integer_Index.append(variable_names.index(Integer_Variable_Names[index_counter]))
        index_counter += 1
    
    Integer_Variable_Name = Integer_Variable_Names


        
# Before soving the problem, firstly record all the input with deep copy in case the variable changes in the following steps

# complete function to copy the input for comparison in further steps
# and summarize inputs

def complete():
    
    global Deep_Copy_objective, Deep_Copy_multi_objective, Deep_Copy_constraint, Deep_Copy_integer_constraint

    def print_frame(*words):
        
        size = max(len(word) for word in words)
        print('\033[1m' + '=' * (size + 6))
        
        for word in words:
            print('\033[1m' + '== {w:<{s}} =='.format(w=word, s=size))
            
        print('\033[1m' + '=' * (size + 6))
    
    print_frame("Summary of", "Settings for: ", obj_names[0])
    
    # summarize objective
    
    try:
        Deep_Copy_objective = copy.deepcopy([obj_names, obj_coef, variable_names, obj_max])
        print("\nYou have set the objective " + str(obj_names[0]) + " to:\n")
        
        print_counter = 0
        
        if obj_max == True:
            print("To Maximise " + str(obj_names[0]) + " = ", end="")
        else:
            print("To Minimise " + str(obj_names[0]) + " = ", end="")
            
        for print_counter in range(len(variable_names)-1):
            print(str(obj_coef[print_counter]) + " * " + str(variable_names[print_counter]) + " + ", end = "")
            print_counter += 1
        print(str(obj_coef[-1]) + " * " + str(variable_names[-1]) + " ; \n")
              
    except NameError:
        print("\n(Note: You havn't set any single objective.)\n")
    
    # summarize multi-objective
              
    try:
        Deep_Copy_multi_objective = copy.deepcopy([multi_obj_names, obj_names, multi_obj_coef, obj_coef, variable_names, multi_obj_max])
        multi_counter = 0
        print_counter = 0
        
        for multi_counter in range(len(multi_obj_names)):
            print("\nYou have set the objective " + str(multi_obj_names[multi_counter]) + " to:\n")
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
              
    except NameError:
        print("\n(Note: You havn't set any other multiple objectives.)\n")
    
    # summarize non-integer constraints
              
    try:
        Deep_Copy_constraint = copy.deepcopy([constraint_names, constraint, bound_names, bound, constraint_type])
        print("\nSubject to: \n")
              
        print_counter = 0
        var_counter = 0
        
        for print_counter in range(len(constraint_names)):
            print(str(constraint_type[print_counter]) + " constraints: " + str(constraint_names[print_counter]) + " : ", end = "")
            for var_counter in range(len(variable_names)-1):
                print(str(Deep_Copy_constraint[1][print_counter][var_counter]) + " * " + str(variable_names[var_counter]) + " + ", end = "")
                var_counter += 1
            print(str(Deep_Copy_constraint[1][print_counter][-1]) + " * " + str(variable_names[-1]) + " <= " + str(bound[print_counter]) + " ; \n")
            print_counter += 1         
              
    except NameError:
        ("\n(Note: You havn't set any non-integer constraints.)\n")
    
    # summarize integer constraints
              
    try:
        Deep_Copy_integer_constraint = copy.deepcopy([Integer_Variable_Name, Integer_Index])
        print("\nYou have set the variables: " + str(Integer_Variable_Name[:]) + " to take only integer values.\n")
    except NameError:
        print("\n(Note: You havn't set any variables to be integer.)\n")
        
    
    print_frame("The End of", "Summary of", "Settings for: ", obj_names[0])
    
    

# The End of Set Module
