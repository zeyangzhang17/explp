# Module: sensitivity_analysis

# Functions:
    # sensitivity_analysis.Optimal_Var()
    # sensitivity_analysis.Obj_Coef()
    # sensitivity_analysis.Con_Bound()
    # sensitivity_analysis.Con_Remove()
    # sensitivity_analysis.Sensitivity_Analysis()

    
    
# Last Updated: 27th July 2018

# Further Improvement:
    # 1. add explanations in sensitivity analysis function



import numpy as np
import pandas as pd
import matplotlib as plt
import copy
from explp import solve


# optimal varible sensitivity analysis function

# Aim to explain why the optimal solution is the best
# By changing optimal solution up and down 1 unit and -100% to +100%, in order to see how the objective changes and whether constraints are violated
    
    
def Optimal_Var(optimal_solution_Simplex):
    
    optimal_solution = copy.deepcopy(optimal_solution_Simplex[:])
    
    optimal_objective_value = optimal_solution[0]
    optimal_variable_value = optimal_solution[1]
    optimal_slack_value = optimal_solution[2]
    
    # introduce a spacing for table
    
    spacing = '...'
    
    # record which constraint is violated if optimal solution + / - 1 & + / - 10-100%
    
    violated_constraint_minus = []
    violated_constraint_plus = []
    
    violated_constraint_m100 = []
    violated_constraint_m50 = []
    violated_constraint_m25 = []
    violated_constraint_m10 = []
    
    violated_constraint_p10 = []
    violated_constraint_p25 = []
    violated_constraint_p50 = []
    violated_constraint_p100 = []
    
    variable_counter = 0
    constraint_counter = 0
    
    for variable_counter in range(len(variable_names)):
        
        # temp list to record violated constraints for a single variable
        # reset to empty for each variable 
        
        temp_list_minus = []
        temp_list_plus = []
        
        temp_list_m100 = []
        temp_list_m50 = []
        temp_list_m25 = []
        temp_list_m10 = []
        
        temp_list_p10 = []
        temp_list_p25 = []
        temp_list_p50 = []
        temp_list_p100 = []
        
        for constraint_counter in range(len(constraint_names)):
            
            if constraint[constraint_counter][variable_counter]*(-1) > optimal_slack_value[constraint_counter]:
                temp_list_minus.append(constraint_names[constraint_counter])
                
            if constraint[constraint_counter][variable_counter]*1 > optimal_slack_value[constraint_counter]:
                temp_list_plus.append(constraint_names[constraint_counter])
                
            if constraint[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(-1) > optimal_slack_value[constraint_counter]:
                temp_list_m100.append(constraint_names[constraint_counter])
            
            if constraint[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(-0.5) > optimal_slack_value[constraint_counter]:
                temp_list_m50.append(constraint_names[constraint_counter])
  
            if constraint[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(-0.25) > optimal_slack_value[constraint_counter]:
                temp_list_m25.append(constraint_names[constraint_counter])
            
            if constraint[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(-0.1) > optimal_slack_value[constraint_counter]:
                temp_list_m10.append(constraint_names[constraint_counter])
                
            if constraint[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(0.1) > optimal_slack_value[constraint_counter]:
                temp_list_p10.append(constraint_names[constraint_counter])
                
            if constraint[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(0.25) > optimal_slack_value[constraint_counter]:
                temp_list_p25.append(constraint_names[constraint_counter])
                
            if constraint[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(0.5) > optimal_slack_value[constraint_counter]:
                temp_list_p50.append(constraint_names[constraint_counter])
                
            if constraint[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(1) > optimal_slack_value[constraint_counter]:
                temp_list_p100.append(constraint_names[constraint_counter])
                
            constraint_counter += 1
        
        # record violated constraints for the variables
        
        violated_constraint_minus.append(temp_list_minus)
        violated_constraint_plus.append(temp_list_plus)
        
        violated_constraint_m100.append(temp_list_m100)
        violated_constraint_m50.append(temp_list_m50)
        violated_constraint_m25.append(temp_list_m25)
        violated_constraint_m10.append(temp_list_m10)
        
        violated_constraint_p10.append(temp_list_p10)
        violated_constraint_p25.append(temp_list_p25)
        violated_constraint_p50.append(temp_list_p50)
        violated_constraint_p100.append(temp_list_p100)
            
        variable_counter += 1
    
    # set empty violated constraints to None
    
    modify_counter = 0
    
    for modify_counter in range(len(variable_names)):
        
        if not violated_constraint_minus[modify_counter]:
            violated_constraint_minus[modify_counter] = None
            
        if not violated_constraint_plus[modify_counter]:
            violated_constraint_plus[modify_counter] = None
        
        if not violated_constraint_m100[modify_counter]:
            violated_constraint_m100[modify_counter] = None
        
        if not violated_constraint_m50[modify_counter]:
            violated_constraint_m50[modify_counter] = None
        
        if not violated_constraint_m25[modify_counter]:
            violated_constraint_m25[modify_counter] = None
        
        if not violated_constraint_m10[modify_counter]:
            violated_constraint_m10[modify_counter] = None
        
        if not violated_constraint_p10[modify_counter]:
            violated_constraint_p10[modify_counter] = None
        
        if not violated_constraint_p25[modify_counter]:
            violated_constraint_p25[modify_counter] = None
        
        if not violated_constraint_p50[modify_counter]:
            violated_constraint_p50[modify_counter] = None
        
        if not violated_constraint_p100[modify_counter]:
            violated_constraint_p100[modify_counter] = None
                
        modify_counter += 1
        
    # form a dataframe to output results
    
    col_var_changes = ['Optimal Solution - 1', 'Optimal Solution', 'Optimal Solution + 1', spacing, 'Optimal Solution - 100%', 'Optimal Solution - 50%', 'Optimal Solution - 25%', 'Optimal Solution - 10%', 'Optimal Solution', 'Optimal Solution + 10%', 'Optimal Solution + 25%', 'Optimal Solution + 50%', 'Optimal Solution + 100%']
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
    
        table_var_changes.iloc[fill_counter,:] = [spacing]*13
        table_var_changes.iloc[fill_counter+1,:] = [optimal_variable_value[int(fill_counter/4)]-1, optimal_variable_value[int(fill_counter/4)], optimal_variable_value[int(fill_counter/4)]+1, spacing, 0, optimal_variable_value[int(fill_counter/4)]*0.5, optimal_variable_value[int(fill_counter/4)]*0.75, optimal_variable_value[int(fill_counter/4)]*0.9, optimal_variable_value[int(fill_counter/4)], optimal_variable_value[int(fill_counter/4)]*1.1, optimal_variable_value[int(fill_counter/4)]*1.25, optimal_variable_value[int(fill_counter/4)]*1.5, optimal_variable_value[int(fill_counter/4)]*2] 
        table_var_changes.iloc[fill_counter+2,:] = [optimal_objective_value-obj_coef[int(fill_counter/4)], optimal_objective_value, optimal_objective_value+obj_coef[int(fill_counter/4)], spacing, optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(-1), optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(-0.5), optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(-0.25), optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(-0.1), optimal_objective_value, optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(0.1), optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(0.25), optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(0.5), optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(1)]
        table_var_changes.iloc[fill_counter+3,0] = violated_constraint_minus[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,1] = None
        table_var_changes.iloc[fill_counter+3,2] = violated_constraint_plus[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,3] = spacing
        table_var_changes.iloc[fill_counter+3,4] = violated_constraint_m100[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,5] = violated_constraint_m50[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,6] = violated_constraint_m25[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,7] = violated_constraint_m10[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,8] = None
        table_var_changes.iloc[fill_counter+3,9] = violated_constraint_p10[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,10] = violated_constraint_p25[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,11] = violated_constraint_p50[int(fill_counter/4)]
        table_var_changes.iloc[fill_counter+3,12] = violated_constraint_p100[int(fill_counter/4)]
        
        negative_counter = 0
        
        for negative_counter in range(13):
            
            # to check if any variables are negative, which will cause infeasible
            
            try:
                if table_var_changes.iloc[fill_counter+1,negative_counter] < 0:
                    table_var_changes.iloc[fill_counter+2,negative_counter] = 'INFESIBLE'
                    table_var_changes.iloc[fill_counter+3,negative_counter] = variable_names[int(fill_counter/4)] + ' >= 0'
                    table_var_changes.iloc[fill_counter+1,negative_counter] = '< 0'
                    
            # since there is a spacing in str, which cannot be compared with 0, so except the TypeError to keep the program running
            
            except:
                TypeError

    
    return table_var_changes

    
    
# objective coefficient sensitivity analysis function

# Still the same bug


def Obj_Coef(obj_coef, optimal_solution_Simplex):
    
    original_obj_coef = copy.deepcopy(obj_coef[:])
    
    original_optimal_solution = copy.deepcopy(optimal_solution_Simplex[:])
    
    new_optimal_minus = []
    new_optimal_plus = []
    
    new_optimal_m100 = []
    new_optimal_m50 = []
    new_optimal_m25 = []
    new_optimal_m10 = []
    
    new_optimal_p10 = []
    new_optimal_p25 = []
    new_optimal_p50 = []
    new_optimal_p100 = []
    
    coef_counter = 0
    
    for coef_counter in range(len(variable_names)):
        
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] -= 1
        obj_minus = Simplex()
        
        if NoFeasibleSolution == True:
            new_optimal_minus.append('INFESIBLE')
        else:
            new_optimal_minus.append(obj_minus[1][0])
            
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] += 1
        obj_plus = Simplex()
        
        if NoFeasibleSolution == True:
            new_optimal_plus.append('INFESIBLE')
        else:
            new_optimal_plus.append(obj_plus[1][0])
        
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = 0
        obj_m100 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_m100.append('INFESIBLE')
        else:
            new_optimal_m100.append(obj_m100[1][0])
        
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*0.5
        obj_m50 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_m50.append('INFESIBLE')
        else:
            new_optimal_m50.append(obj_m50[1][0])

        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*0.75
        obj_m25 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_m25.append('INFESIBLE')
        else:
            new_optimal_m25.append(obj_m25[1][0])    
            
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*0.9
        obj_m10 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_m10.append('INFESIBLE')
        else:
            new_optimal_m10.append(obj_m10[1][0])
            
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*1.1
        obj_p10 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_p10.append('INFESIBLE')
        else:
            new_optimal_p10.append(obj_p10[1][0])
        
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*1.25
        obj_p25 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_p25.append('INFESIBLE')
        else:
            new_optimal_p25.append(obj_p25[1][0])

        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*1.5
        obj_p50 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_p50.append('INFESIBLE')
        else:
            new_optimal_p50.append(obj_p50[1][0])
            
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*2
        obj_p100 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_p100.append('INFESIBLE')
        else:
            new_optimal_p100.append(obj_p100[1][0]) 
        
        #
        
        coef_counter += 1
    
    spacing = '...'
    
    col_obj_coef = ['Coefficient - 1', 'Coefficient', 'Coefficient + 1', spacing, 'Coefficient - 100%', 'Coefficient - 50%', 'Coefficient - 25%', 'Coefficient - 10%', 'Coefficient', 'Coefficient + 10%', 'Coefficient + 25%', 'Coefficient + 50%', 'Coefficient + 100%']
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
    
        table_obj_coef.iloc[fill_counter,:] = [spacing]*13
        table_obj_coef.iloc[fill_counter+1,:] = [original_obj_coef[int(fill_counter/4)]-1, original_obj_coef[int(fill_counter/4)], original_obj_coef[int(fill_counter/4)]+1, spacing, 0, original_obj_coef[int(fill_counter/4)]*0.5, original_obj_coef[int(fill_counter/4)]*0.75, original_obj_coef[int(fill_counter/4)]*0.9, original_obj_coef[int(fill_counter/4)], original_obj_coef[int(fill_counter/4)]*1.1, original_obj_coef[int(fill_counter/4)]*1.25, original_obj_coef[int(fill_counter/4)]*1.5, original_obj_coef[int(fill_counter/4)]*2] 
        table_obj_coef.iloc[fill_counter+2,:] = [new_optimal_minus[int(fill_counter/4)], original_optimal_solution[0], new_optimal_plus[int(fill_counter/4)], spacing, new_optimal_m100[int(fill_counter/4)], new_optimal_m50[int(fill_counter/4)], new_optimal_m25[int(fill_counter/4)], new_optimal_m10[int(fill_counter/4)], original_optimal_solution[0], new_optimal_p10[int(fill_counter/4)], new_optimal_p25[int(fill_counter/4)], new_optimal_p50[int(fill_counter/4)], new_optimal_p100[int(fill_counter/4)]]
        
        infeasible_counter = 0
        
        for infeasible_counter in range(13):
            if table_obj_coef.iloc[fill_counter+2,infeasible_counter] == 'INFESIBLE':
                table_obj_coef.iloc[fill_counter+3,infeasible_counter] = 'INFESIBLE'
            else:
                table_obj_coef.iloc[fill_counter+3,0] = table_obj_coef.iloc[fill_counter+2,0] - table_obj_coef.iloc[fill_counter+2,1]
                table_obj_coef.iloc[fill_counter+3,1] = None
                table_obj_coef.iloc[fill_counter+3,2] = table_obj_coef.iloc[fill_counter+2,2] - table_obj_coef.iloc[fill_counter+2,1]
                table_obj_coef.iloc[fill_counter+3,3] = spacing
                
                for perc_fill_counter in range(4,13):
                    table_obj_coef.iloc[fill_counter+3,perc_fill_counter] = table_obj_coef.iloc[fill_counter+2,perc_fill_counter] - table_obj_coef.iloc[fill_counter+2,1]
                    perc_fill_counter += 1
                                              
                table_obj_coef.iloc[fill_counter+3,8] = None

    
    return table_obj_coef


    
# constraint bound sensitivity analysis function

# mostly similar to objective coefficient sensitivity analysis function


def Con_Bound(bound, optimal_solution_Simplex): 
    
    original_con_bound = copy.deepcopy(bound[:])
    
    original_optimal_solution = copy.deepcopy(optimal_solution_Simplex[:])
    
    new_optimal_minus = []
    new_optimal_plus = []
    
    new_optimal_m100 = []
    new_optimal_m50 = []
    new_optimal_m25 = []
    new_optimal_m10 = []
    
    new_optimal_p10 = []
    new_optimal_p25 = []
    new_optimal_p50 = []
    new_optimal_p100 = []
    
    bound_counter = 0
    
    for bound_counter in range(len(constraint_names)):
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] -= 1
        bound_minus = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_minus.append('INFESIBLE')
        else:
            new_optimal_minus.append(bound_minus[1][0])
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] += 1
        bound_plus = Simplex()
        
        if NoFeasibleSolution == True:
            new_optimal_plus.append('INFESIBLE')
        else:
            new_optimal_plus.append(bound_plus[1][0])
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = 0
        bound_m100 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_m100.append('INFESIBLE')
        else:
            new_optimal_m100.append(bound_m100[1][0])
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*0.5
        bound_m50 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_m50.append('INFESIBLE')
        else:
            new_optimal_m50.append(bound_m50[1][0])

        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*0.75
        bound_m25 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_m25.append('INFESIBLE')
        else:
            new_optimal_m25.append(bound_m25[1][0])    
            
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*0.9
        bound_m10 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_m10.append('INFESIBLE')
        else:
            new_optimal_m10.append(bound_m10[1][0])
            
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*1.1
        bound_p10 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_p10.append('INFESIBLE')
        else:
            new_optimal_p10.append(bound_p10[1][0])
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*1.25
        bound_p25 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_p25.append('INFESIBLE')
        else:
            new_optimal_p25.append(bound_p25[1][0])

        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*1.5
        bound_p50 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_p50.append('INFESIBLE')
        else:
            new_optimal_p50.append(bound_p50[1][0])
            
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*2
        bound_p100 = Simplex()   
        
        if NoFeasibleSolution == True:
            new_optimal_p100.append('INFESIBLE')
        else:
            new_optimal_p100.append(bound_p100[1][0])   
               
        #
        
        bound_counter += 1
    
    spacing = '...'
    
    col_bound = ['Bound Value - 1', 'Bound Value', 'Bound Value + 1', spacing, 'Bound Value - 100%', 'Bound Value - 50%', 'Bound Value - 25%', 'Bound Value - 10%', 'Bound Value', 'Bound Value + 10%', 'Bound Value + 25%', 'Bound Value + 50%', 'Bound Value + 100%']
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
    
        table_bound.iloc[fill_counter,:] = [spacing]*13
        table_bound.iloc[fill_counter+1,:] = [original_con_bound[int(fill_counter/4)]-1, original_con_bound[int(fill_counter/4)], original_con_bound[int(fill_counter/4)]+1, spacing, 0, original_con_bound[int(fill_counter/4)]*0.5, original_con_bound[int(fill_counter/4)]*0.75, original_con_bound[int(fill_counter/4)]*0.9, original_con_bound[int(fill_counter/4)], original_con_bound[int(fill_counter/4)]*1.1, original_con_bound[int(fill_counter/4)]*1.25, original_con_bound[int(fill_counter/4)]*1.5, original_con_bound[int(fill_counter/4)]*2]
        table_bound.iloc[fill_counter+2,:] = [new_optimal_minus[int(fill_counter/4)], original_optimal_solution[0], new_optimal_plus[int(fill_counter/4)], spacing, new_optimal_m100[int(fill_counter/4)], new_optimal_m50[int(fill_counter/4)], new_optimal_m25[int(fill_counter/4)], new_optimal_m10[int(fill_counter/4)], original_optimal_solution[0], new_optimal_p10[int(fill_counter/4)], new_optimal_p25[int(fill_counter/4)], new_optimal_p50[int(fill_counter/4)], new_optimal_p100[int(fill_counter/4)]]
        
        infeasible_counter = 0
        
        for infeasible_counter in range(13):
            if table_bound.iloc[fill_counter+2,infeasible_counter] == 'INFESIBLE':
                table_bound.iloc[fill_counter+3,infeasible_counter] = 'INFESIBLE'                                     
                                              
            else:
                table_bound.iloc[fill_counter+3,0] = table_bound.iloc[fill_counter+2,0] - table_bound.iloc[fill_counter+2,1]
                table_bound.iloc[fill_counter+3,1] = None
                table_bound.iloc[fill_counter+3,2] = table_bound.iloc[fill_counter+2,2] - table_bound.iloc[fill_counter+2,1]
                table_bound.iloc[fill_counter+3,3] = spacing
                                              
                for perc_fill_counter in range(4,13):
                    table_bound.iloc[fill_counter+3,perc_fill_counter] = table_bound.iloc[fill_counter+2,perc_fill_counter] - table_bound.iloc[fill_counter+2,1]
                    perc_fill_counter += 1
                                              
                table_bound.iloc[fill_counter+3,8] = None

        # constraint bound less than 0 is not making sense
        
        if table_bound.iloc[fill_counter+1,0] < 0:
            table_bound.iloc[fill_counter+1,0] = 'INFESIBLE'
            table_bound.iloc[fill_counter+2,0] = 'INFESIBLE'
            table_bound.iloc[fill_counter+3,0] = 'INFESIBLE'
                
    
    return table_bound
    
    
    
# constraint remove sensitivity analysis function

def Con_Remove(constraint_names, constraint, bound, optimal_solution_Simplex):
    
    original_optimal_solution = copy.deepcopy(optimal_solution_Simplex[:])
    
    original_constraint_names = copy.deepcopy(constraint_names[:])
    original_constraint = copy.deepcopy(constraint[:])
    original_bound = copy.deepcopy(bound[:])
    
    soft_con_index = []
    
    soft_con_counter = 0
    
    for soft_con_counter in range(len(original_constraint_names)):
        if constraint_type[soft_con_counter] == 'soft':
            soft_con_index.append(soft_con_counter)
            soft_con_counter += 1
            
    if len(soft_con_index) == 0:
        
        # if no soft constraints, then no constraints can be removed
        
        table_con_remove = None
        print('There are no soft constraints to be removed.')
        
        return table_con_remove
    
    else:
        
        # remove each soft constraints to see the changes, similiar to the previous procedures
        
        optimal_excl_soft = []
        
        for soft_con_remove_counter in soft_con_index:
            
            constraint_names = copy.deepcopy(original_constraint_names)
            constraint = copy.deepcopy(original_constraint)
            bound = copy.deepcopy(original_bound)
            
            del constraint_names[soft_con_remove_counter]
            del constraint[soft_con_remove_counter]
            del bound[soft_con_remove_counter]
            
            Simplex_excl_soft = Simplex()
            
            if NoFeasibleSolution == True:
                optimal_excl_soft.append('INFESIBLE')
            else:            
                optimal_excl_soft.append(Simplex_excl_soft[1][0])
        
        spacing = '...'

        col_con_remove = ['Original', 'After Removal']
        row_con_remove = []

        row_counter = 0

        for row_counter in range(len(soft_con_index)):
            row_con_remove.append(spacing)
            row_con_remove.append('Remove of soft constraint ' + original_constraint_names[soft_con_index[row_counter]])
            row_con_remove.append('Value of ' + obj_names[0])
            row_con_remove.append('Changes in Objective Values')
            row_counter += 1

        row_con_remove.append(spacing)

        table_con_remove = pd.DataFrame(columns = col_con_remove, index = row_con_remove).fillna('')

        fill_counter = 0

        for fill_counter in range(0,4*(len(soft_con_index)-1)+1,4):

            table_con_remove.iloc[fill_counter,:] = [spacing]*2
            table_con_remove.iloc[fill_counter+1,:] = ' '
            table_con_remove.iloc[fill_counter+2,:] = [original_optimal_solution[0], optimal_excl_soft[int(fill_counter/4)]]

            infeasible_counter = 0

            for infeasible_counter in range(2):
                if table_con_remove.iloc[fill_counter+2,infeasible_counter] == 'INFESIBLE':
                    table_con_remove.iloc[fill_counter+3,infeasible_counter] = 'INFESIBLE'
                else:
                    table_con_remove.iloc[fill_counter+3,0] = None
                    table_con_remove.iloc[fill_counter+3,1] = table_con_remove.iloc[fill_counter+2,1] - table_con_remove.iloc[fill_counter+2,0]


    return table_con_remove
    
    
    
# Sensitivity Analysis function to run different sets of sensitivity analysis based on various situations
# And output explanations

def Sensitivity_Analysis():
    
    

    
    
Sensitivity_Analysis()


# The End of Sensitivity Analysis Module
