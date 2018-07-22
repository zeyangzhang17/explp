# Module: sensitivity_analysis

# Functions:
    # sensitivity_analysis.Optimal_Var()
    # sensitivity_analysis.Obj_Coef()
    # sensitivity_analysis.Con_Bound()
    # sensitivity_analysis.Con_Remove()
    # sensitivity_analysis.Sensitivity_Analysis()

    
    
# Last Updated: 22nd July 2018



import numpy as np
import pandas as pd
import matplotlib as plt
from explp import solve


# optimal varible sensitivity analysis function

# Potential further improvement: percentage changes

# Aim to explain why the optimal solution is the best
# By changing optimal solution up and down 1 unit to see how the objective changes and whether constraints are violated
    
def Optimal_Var():
    
    optimal_solution = optimal_solution_Simplex[:]
    
    optimal_objective_value = optimal_solution[0]
    optimal_variable_value = optimal_solution[1]
    optimal_slack_value = optimal_solution[2]
    
    # introduce a spacing for table
    
    spacing = '...'
    
    # record which constraint is violated if optimal solution + / - 1
    
    violated_constraint_minus = []
    violated_constraint_plus = []
    
    variable_counter = 0
    constraint_counter = 0
    
    for variable_counter in range(len(variable_names)):
        
        # temp list to record violated constraints for a single variable
        # reset to empty for each variable 
        
        temp_list_minus = []
        temp_list_plus = []
        
        for constraint_counter in range(len(constraint_names)):
            
            if constraint[constraint_counter][variable_counter]*(-1) > optimal_slack_value[constraint_counter]:
                temp_list_minus.append(constraint_names[constraint_counter])
                
            if constraint[constraint_counter][variable_counter]*1 > optimal_slack_value[constraint_counter]:
                temp_list_plus.append(constraint_names[constraint_counter])
                
            constraint_counter += 1
        
        # record violated constraints for the variables
        
        violated_constraint_minus.append(temp_list_minus)
        violated_constraint_plus.append(temp_list_plus)
            
        variable_counter += 1
    
    # set empty violated constraints to None
    
    modify_counter = 0
    
    for modify_counter in range(len(variable_names)):
        
        if not violated_constraint_minus[modify_counter]:
            violated_constraint_minus[modify_counter] = None
        
        if not violated_constraint_plus[modify_counter]:
            violated_constraint_plus[modify_counter] = None
                
        modify_counter += 1
        
    # form a dataframe to output results
    
    col_var_changes = ['Optimal Solution - 1', 'Optimal Solution', 'Optimal Solution + 1']
    row_var_changes = []
    
    row_counter = 0
    
    for row_counter in range(len(variable_names)):
        
        # add line spacing for a better view
        
        row_var_changes.append(spacing)
        row_var_changes.append('Value of ' + variable_names[row_counter])
        row_var_changes.append('Value of ' + obj_names[0])
        row_var_changes.append('Violated Constraints')
        row_counter += 1
        
    row_var_changes.append(spacing)
    
    # fill in the numbers and violated constraints, and fill NaN with empty
    
    table_var_changes = pd.DataFrame(columns = col_var_changes, index = row_var_changes).fillna('')
    
    fill_counter = 0
    
    for fill_counter in range(0,4*(len(variable_names)-1)+1,4):
    
        table_var_changes.iloc[fill_counter,:] = [spacing]*3
        table_var_changes.iloc[fill_counter+1,:] = [optimal_variable_value[int(fill_counter/4)]-1, optimal_variable_value[int(fill_counter/4)], optimal_variable_value[int(fill_counter/4)]+1] 
        table_var_changes.iloc[fill_counter+2,:] = [optimal_objective_value-obj_coef[int(fill_counter/4)], optimal_objective_value, optimal_objective_value+obj_coef[int(fill_counter/4)]]
        table_var_changes.iloc[fill_counter+3,0] = violated_constraint_minus[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,1] = None
        table_var_changes.iloc[fill_counter+3,2] = violated_constraint_plus[int(fill_counter/4)]
        
        negative_counter = 0
        
        for negative_counter in range(3):
            
            # to check if any variables are negative, which will cause infeasible
            
            if table_var_changes.iloc[fill_counter+1,negative_counter] < 0:
                table_var_changes.iloc[fill_counter+2,negative_counter] = 'INFESIBLE'
                table_var_changes.iloc[fill_counter+3,negative_counter] = variable_names[int(fill_counter/4)] + ' >= 0'
                table_var_changes.iloc[fill_counter+1,negative_counter] = '< 0'
    
    
    return table_var_changes
    
    
    
# objective coefficient sensitivity analysis function

# Potential further improvement: percentage changes

def Obj_Coef():
    
    original_obj_coef = obj_coef[:]
    
    original_optimal_solution = optimal_solution_Simplex[:]
    
    new_optimal_minus = []
    new_optimal_plus = []
    
    coef_counter = 0
    
    for coef_counter in range(len(variable_names)):
        
        obj_coef = original_obj_coef
        obj_coef[coef_counter] -= 1
        obj_minus = Simplex()
        
        if NoFeasibleSolution == True:
            new_optimal_minus.append('INFESIBLE')
        else:
            new_optimal_minus.append(obj_minus[1][0])
        
        obj_coef = original_obj_coef
        obj_coef[coef_counter] += 1
        obj_plus = Simplex()
        
        if NoFeasibleSolution == True:
            new_optimal_plus.append('INFESIBLE')
        else:
            new_optimal_plus.append(obj_plus[1][0])
        
        coef_counter += 1
    
    spacing = '...'
    
    col_obj_coef = ['Coefficient - 1', 'Coefficient', 'Coefficient + 1']
    row_obj_coef = []
    
    row_counter = 0
    
    for row_counter in range(len(variable_names)):
        row_obj_coef.append(spacing)
        row_obj_coef.append('Coefficients of ' + variable_names[row_counter])
        row_obj_coef.append('Value of ' + obj_names[0])
        row_obj_coef.append('Changes in Objective Values')
        row_counter += 1
        
    row_obj_coef.append(spacing)
    
    table_obj_coef = pd.DataFrame(columns = col_obj_coef, index = row_obj_coef).fillna('')
    
    fill_counter = 0
    
    for fill_counter in range(0,4*(len(variable_names)-1)+1,4):
    
        table_obj_coef.iloc[fill_counter,:] = [spacing]*3
        table_obj_coef.iloc[fill_counter+1,:] = [original_obj_coef[int(fill_counter/4)]-1, original_obj_coef[int(fill_counter/4)], original_obj_coef[int(fill_counter/4)]+1] 
        table_obj_coef.iloc[fill_counter+2,:] = [new_optimal_minus[int(fill_counter/4)], original_optimal_solution[0], new_optimal_plus[int(fill_counter/4)]]
        table_obj_coef.iloc[fill_counter+3,0] = table_obj_coef.iloc[fill_counter+2,0] - table_obj_coef.iloc[fill_counter+2,1]
        table_obj_coef.iloc[fill_counter+3,1] = 0
        table_obj_coef.iloc[fill_counter+3,2] = table_obj_coef.iloc[fill_counter+2,2] - table_obj_coef.iloc[fill_counter+2,1]
        
        infeasible_counter = 0
        
        for negative_counter in range(3):
            if table_obj_coef.iloc[fill_counter+2,infeasible_counter] == 'INFESIBLE':
                table_obj_coef.iloc[fill_counter+3,infeasible_counter] = 'INFESIBLE'
    
    
    return table_obj_coef


    
# constraint bound sensitivity analysis function

# mostly similar to objective coefficient sensitivity analysis function

def Con_Bound(): 
    
    original_con_bound = bound[:]
    
    original_optimal_solution = optimal_solution_Simplex[:]
    
    new_optimal_minus = []
    new_optimal_plus = []
    
    bound_counter = 0
    
    for bound_counter in range(len(constraint_names)):
        
        bound = original_con_bound
        
        bound[bound_counter] -= 1
        obj_minus = Simplex()   
        
        
        if NoFeasibleSolution == True:
            new_optimal_minus.append('INFESIBLE')
        else:
            new_optimal_minus.append(obj_minus[1][0])
        
        bound = original_con_bound
        bound[bound_counter] += 1
        obj_plus = Simplex()
        
        if NoFeasibleSolution == True:
            new_optimal_plus.append('INFESIBLE')
        else:
            new_optimal_plus.append(obj_plus[1][0])
        
        bound_counter += 1
    
    spacing = '...'
    
    col_bound = ['Bound Value - 1', 'Bound Value', 'Bound Value + 1']
    row_bound = []
    
    row_counter = 0
    
    for row_counter in range(len(constraint_names)):
        row_bound.append(spacing)
        row_bound.append('Bound of ' + constraint_names[row_counter])
        row_bound.append('Value of ' + obj_names[0])
        row_bound.append('Changes in Objective Values')
        row_counter += 1
        
    row_bound.append(spacing)
    
    table_bound = pd.DataFrame(columns = col_bound, index = row_bound).fillna('')
    
    fill_counter = 0
    
    for fill_counter in range(0,4*(len(constraint_names)-1)+1,4):
    
        table_bound.iloc[fill_counter,:] = [spacing]*3
        table_bound.iloc[fill_counter+1,:] = [original_con_bound[int(fill_counter/4)]-1, original_con_bound[int(fill_counter/4)], original_con_bound[int(fill_counter/4)]+1] 
        table_bound.iloc[fill_counter+2,:] = [new_optimal_minus[int(fill_counter/4)], original_optimal_solution[0], new_optimal_plus[int(fill_counter/4)]]
        table_bound.iloc[fill_counter+3,0] = table_bound.iloc[fill_counter+2,0] - table_bound.iloc[fill_counter+2,1]
        table_bound.iloc[fill_counter+3,1] = 0
        table_bound.iloc[fill_counter+3,2] = table_bound.iloc[fill_counter+2,2] - table_bound.iloc[fill_counter+2,1]
        
        infeasible_counter = 0
        
        for negative_counter in range(3):
            if table_bound.iloc[fill_counter+2,infeasible_counter] == 'INFESIBLE':
                table_bound.iloc[fill_counter+3,infeasible_counter] = 'INFESIBLE'
        
        # constraint bound less than 0 is not making sense
        
        if table_bound.iloc[fill_counter+1,0] < 0:
            table_bound.iloc[fill_counter+2,0] = 'INFESIBLE'
            table_bound.iloc[fill_counter+3,0] = 'INFESIBLE'
            
    
    
    return table_bound

    
    
    
# constraint remove sensitivity analysis function

def Con_Remove():
    

    
    
# Sensitivity Analysis function to run different sets of sensitivity analysis based on various situations
# And output explanations

def Sensitivity_Analysis():
    

    
    
Sensitivity_Analysis()


# The End of Sensitivity Analysis Module
