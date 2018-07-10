# Module: sensitivity_analysis

# Functions:
    # sensitivity_analysis.optimal_var()
    # sensitivity_analysis.obj_coef()
    # sensitivity_analysis.con_bound()
    # sensitivity_analysis.con_coef()
    # sensitivity_analysis.SA()

    
    
# Last Updated: 10th July 2018



import numpy as np
import pandas as pd
import matplotlib as plt
from explp import solve


# optimal varible sensitivity analysis function
# Aim to explain why the optimal solution is the best
# By changing optimal solution up and down 1 unit to see how the objective changes and whether constraints are violated
    
def optimal_var():
    
    global table_var_changes
    
    optimal_solution = optimal_solution_Simplex.copy()
    
    optimal_objective_value = optimal_solution[0]
    optimal_variable_value = optimal_solution[1]
    optimal_slack_value = optimal_solution[2]
    
    spacing = '...'
    
    violated_constraint_minus = []
    violated_constraint_plus = []
    
    variable_counter = 0
    constraint_counter = 0
    
    for variable_counter in range(len(variable_names)):
        
        temp_list_minus = []
        temp_list_plus = []
        
        for constraint_counter in range(len(constraint_names)):
            
            if constraint[constraint_counter][variable_counter]*(-1) > optimal_slack_value[constraint_counter]:
                temp_list_minus.append(constraint_names[constraint_counter])
                
            if constraint[constraint_counter][variable_counter]*1 > optimal_slack_value[constraint_counter]:
                temp_list_plus.append(constraint_names[constraint_counter])
                
            constraint_counter += 1
        
        violated_constraint_minus.append(temp_list_minus)
        violated_constraint_plus.append(temp_list_plus)
            
        variable_counter += 1
    
    modify_counter = 0
    
    for modify_counter in range(len(variable_names)):
        
        if not violated_constraint_minus[modify_counter]:
            violated_constraint_minus[modify_counter] = None
        
        if not violated_constraint_plus[modify_counter]:
            violated_constraint_plus[modify_counter] = None
                
        modify_counter += 1
        
    
    col_var_changes = ['Optimal Solution - 1', 'Optimal Solution', 'Optimal Solution + 1']
    row_var_changes = []
    
    row_counter = 0
    
    for row_counter in range(len(variable_names)):
        row_var_changes.append(spacing)
        row_var_changes.append('Value of ' + variable_names[row_counter])
        row_var_changes.append('Value of ' + obj_names[0])
        row_var_changes.append('Violated Constraints')
        row_counter += 1
        
    row_var_changes.append(spacing)
    
    table_var_changes = pd.DataFrame(columns = col_var_changes, index = row_var_changes).fillna('')
    
    fill_counter = 0
    
    for fill_counter in range(0,4*(len(variable_names)-1)+1,4):
        
        index_counter = fill_counter
    
        table_var_changes.iloc[fill_counter,:] = [spacing]*3
        table_var_changes.iloc[fill_counter+1,:] = [optimal_variable_value[int(fill_counter/4)]-1, optimal_variable_value[int(fill_counter/4)], optimal_variable_value[int(fill_counter/4)]+1] 
        table_var_changes.iloc[fill_counter+2,:] = [optimal_objective_value-obj_coef[int(fill_counter/4)], optimal_objective_value, optimal_objective_value+obj_coef[int(fill_counter/4)]]
        table_var_changes.iloc[fill_counter+3,0] = violated_constraint_minus[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,1] = None
        table_var_changes.iloc[fill_counter+3,2] = violated_constraint_plus[int(fill_counter/4)]
        
        negative_counter = 0
        
        for negative_counter in range(3):
            if table_var_changes.iloc[fill_counter+1,negative_counter] < 0:
                table_var_changes.iloc[fill_counter+2,negative_counter] = 'INFESIBLE'
                table_var_changes.iloc[fill_counter+3,negative_counter] = variable_names[int(fill_counter/4)] + ' >= 0'
                table_var_changes.iloc[fill_counter+1,negative_counter] = '< 0'
    
    
    return table_var_changes
    
    
    
# objective coefficient sensitivity analysis function

def obj_coef():



    
# constraint bound sensitivity analysis function

def con_bound():

    
    
    
    
# constraint coefficient sensitivity analysis function

def con_coef():
    

    
    
# SA function to run different sets of sensitivity analysis based on various situations
# And output explanations

def SA():
    

    
    
SA()


# The End of Sensitivity Analysis Module
