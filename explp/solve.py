# Module: solve

# Functions: 
    # solve.Simplex()
    # solve.Branch_And_Bound()
    # solve.Solve()

    
    
# Last Updated: 9th July 2018

# Non-completed Parts:

# 1. Simplex Algorithm:    
    # Explanations of Infeasible Solution caused by contradicting constraints
    
# 2. Branch and Bound Algorithm:
    # Not yet completed


import math
import pandas as pd
import numpy as np


def Simplex():
    
    # count for variables and constraints for further uses
    
    var_count = len(variable_names)
    con_count = len(constraint_names)
    
    # setting up the top row of pivoting table (objective rows)
    
    obj_coef_negative = [-value for value in obj_coef]
    
    obj_coef_df = [0] + obj_coef_negative
    objective_dataframe = {obj_names[0]:obj_coef_df}

    objective_index = bound_names + variable_names
    
    # setting up constraints rows
    
    constraint_dataframe = {}
    counter_constraint = 0

    for counter_constriant in range(con_count):
        constraint_dataframe.update({constraint_names[counter_constriant]:constraint[counter_constriant]})
        counter_constraint += 1
    
    # introduce slack variables
    
    slack_var = np.identity(con_count)

    slack_var_names = []
    counter_names = 0
    
    # name the slack variables
    
    for counter_names in range(len(constraint)):
        slack_var_names.append('slack_' + str(constraint_names[counter_names]))
        counter_names += 1
    
    # put all into DataFrame to generate a pivot table
    
    DF_objective = pd.DataFrame(data=objective_dataframe, index=objective_index).T

    DF_constraint = pd.DataFrame(data=constraint_dataframe, index=variable_names).T

    DF_slack_var = pd.DataFrame(data=slack_var, columns=slack_var_names, index=constraint_names)

    DF_bound = pd.DataFrame(data=bound, columns=bound_names, index=constraint_names)
    
    tableau_no_obj = pd.concat([DF_bound, DF_constraint, DF_slack_var], axis=1)
    
    tableau_all = pd.concat([DF_objective, tableau_no_obj]).fillna(0)
    tableau = tableau_all[objective_index + slack_var_names]

    # Basic Feasible Solution in normal cases (actually not useful): [[Obj_value], [var_value], [slack_value]]
    
    BFS = [tableau.iloc[0,0], [0] * var_count, bound]
    
    # creating pivot table
    
    pivoting = tableau.copy()
    
    pivoting_col_list = list(pivoting)
    
    # add a time counter for the times of iterating
    
    times_counter = 0
    pivot_column_record = []
    pivot_row_record = []
    NoFeasibleSolution = False
    
    # if any reduced costs (negative of objective coefficients) are negative:
    
    while any(pivoting.iloc[0,1:var_count+1].values<0) == True:
        
        times_counter += 1
    
        # choose pivot column: the most negative value of reduced costs
        
        pivot_column = pivoting.iloc[0,1:var_count+1].values.tolist().index(min(pivoting.iloc[0,1:var_count+1])) + 1
        pivot_column_record.append(pivot_column)
        
        # compute test ratio (bound / pivot column) and select the smallest
        
        test_ratios = []
        pt_i = 1

        for pt_i in range(1,con_count+1):
            try:
                ratio = pivoting[bound_names[0]][pt_i]/pivoting[pivoting_col_list[pivot_column]][pt_i]
            except ZeroDivisionError:
                ratio = 0
            test_ratios.append(ratio)
            pt_i += 1
        
        if all(ratio <= 0 for ratio in test_ratios) == True:
            NoFeasibleSolution = True
            print('Error! The Problem is UN-BOUNDED !')
            break                
        
        pivot_row = test_ratios.index(min([ratio for ratio in test_ratios if ratio > 0]))+1
        pivot_row_record.append(pivot_row)
        
        pivot_value = pivoting.iloc[pivot_row, pivot_column]
        
        # set pivot value to 1 by dividing the pivot row by pivot value, for further computing
        
        pivoting.iloc[pivot_row,:] = pivoting.iloc[pivot_row,:] / pivot_value
        
        # elementary row operations
        
        pi_count = 0
        
        for pi_count in range(con_count+1):
            if pi_count != pivot_row:
                pivoting.iloc[pi_count,:] = pivoting.iloc[pi_count,:] - pivoting.iloc[pi_count, pivot_column] * pivoting.iloc[pivot_row,:]
                pi_count += 1
            else:
                continue
        
        # prevent possible cycling problems to run infinitely
        
        if times_counter >= 1000:
            print('Error! Too Many Iterations! Maybe caused by the cycling Pivoting Table !')
            NoFeasibleSolution = True
            break
    
    obj_optimal = pivoting.iloc[0,0]
    
    # compute slack value in optimal solution
    
    slack_optimal = pivoting.iloc[1:,0].tolist()
    
    slack_counter = 0
    
    for slack_counter in range(len(pivot_row_record)):
        slack_optimal[pivot_row_record[slack_counter]-1] = 0
        slack_counter += 1
    
    # compute variable value in optimal solution
    
    var_optimal = [0] * var_count
    
    var_counter = 0
    
    for var_counter in range(len(pivot_row_record)):
        var_optimal[pivot_column_record[var_counter]-1] = pivoting.iloc[pivot_row_record[var_counter],0]
        var_counter += 1
    
    optimal_solution_Simplex = [obj_optimal, var_optimal, slack_optimal]
    
    if NoFeasibleSolution == True:
        print('\nThere is NO Feasible Solutions!\n')
        return NoFeasibleSolution
    else:
        return optimal_solution_Simplex


# Branch_And_Bound Function:

def Branch_And_Bound():
    
    # firstly do relaxation of all integer constraints 
    # i.e. to use Simplex algorithm to find global optimal as upper bound
    
    Simplex()
    
    # Non integer-constrained solution -- objective value and variable coefficient
    
    non_int_con_sol_obj = optimal_solution_Simplex[0]
    non_int_con_sol_var = optimal_solution_Simplex[1]
    non_int_con_sol_slack = optimal_solution_Simplex[2]
    
    # record all interger constrained variables
    
    int_con_sol_var = []
    
    for integer_index in Integer_Index:
        int_con_sol_var.append(optimal_solution_Simplex[1][integer_index])
        
    # check if all required integer constraint is satisfied
        
    def list_int_checker(List=[]):
    
        # check if all items in the list are met with integer constraints
    
        int_list = [x = int(x) for x in List]
        
        int_counter = 0
    
        while int_counter in range(len(int_list)):
            
            # check if all integer constraints are met
            
            if int_list[int_counter] == int_con_sol_var[int_counter]:
                all_int = True
                int_counter +=1
                
            # if not, return the index of the first non-integer
            
            else:
                all_int = False
                break
            
            return all_int, int_counter
    
    list_int_checker(int_con_sol_var)
    
    while all_int == False:
        
        
        
        
        
        
        
        
    
    
            
        
        
        
        
        
         
        
        
    obj_BB = non_int_con_sol_obj
    var_BB = non_int_con_sol_var
    slack_BB = non_int_con_sol_slack
        
    optimal_solution_Branch_and_Bound = [obj_BB, var_BB, slack_BB]  
        
    print('All integer constraints are met!')
    return optimal_solution_Branch_and_Bound



# Solve Function:

def Solve():
    
    # check if integer constraints exist
    # run Simplex Algorithm if not, run Branch and Bound Algorithm otherwise
    
    try:
        Integer_Variable_Name
    except NameError:
        return Simplex()
    else: 
        return Branch_And_Bound()

    
Solve()


# The End of Solve Module
