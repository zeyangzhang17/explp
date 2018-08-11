# Module: sensitivity_analysis

# Functions:
    # sensitivity_analysis.Optimal_Var()
    # sensitivity_analysis.Obj_Coef()
    # sensitivity_analysis.Con_Bound()
    # sensitivity_analysis.Con_Remove()
    # sensitivity_analysis.Sensitivity_Analysis()
    
    # sensitivity_analysis.MI_Optimal_Var()
    # sensitivity_analysis.MI_Obj_Coef()
    # sensitivity_analysis.MI_Con_Bound()
    # sensitivity_analysis.MI_Con_Remove()
    # sensitivity_analysis.MI_Sensitivity_Analysis()

    
    
# Last Updated: 11th August 2018



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
from explp import solve



# Firstly to record Optimal Solution
try: 
    optimal_solution_Branch_and_Bound = copy.deepcopy(Deep_Copy_Branch_and_Bound)
except NameError:
    NoFeasibleSolution = True    

    try:
        optimal_solution_Simplex = copy.deepcopy(Deep_Copy_Simplex)
    except NameError:
        NoFeasibleSolution = True
    else:
        tableau = copy.deepcopy(Deep_Copy_tableau)
        NoFeasibleSolution = False
    
    
# optimal varible sensitivity analysis function

# Aim to explain why the optimal solution is the best
# By changing optimal solution up and down 1 unit and -100% to +100%, in order to see how the objective changes and whether constraints are violated
    
def Optimal_Var(optimal_solution_Simplex):
    
    global table_var_changes
    
    optimal_solution = copy.deepcopy(optimal_solution_Simplex[:])
    constraint_value = copy.deepcopy(Deep_Copy_constraint[1])
    
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
            
            if constraint_value[constraint_counter][variable_counter]*(-1) > optimal_slack_value[constraint_counter]:
                temp_list_minus.append(constraint_names[constraint_counter])
                
            if constraint_value[constraint_counter][variable_counter]*1 > optimal_slack_value[constraint_counter]:
                temp_list_plus.append(constraint_names[constraint_counter])
                
            if constraint_value[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(-1) > optimal_slack_value[constraint_counter]:
                temp_list_m100.append(constraint_names[constraint_counter])
            
            if constraint_value[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(-0.5) > optimal_slack_value[constraint_counter]:
                temp_list_m50.append(constraint_names[constraint_counter])
  
            if constraint_value[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(-0.25) > optimal_slack_value[constraint_counter]:
                temp_list_m25.append(constraint_names[constraint_counter])
            
            if constraint_value[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(-0.1) > optimal_slack_value[constraint_counter]:
                temp_list_m10.append(constraint_names[constraint_counter])
                
            if constraint_value[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(0.1) > optimal_slack_value[constraint_counter]:
                temp_list_p10.append(constraint_names[constraint_counter])
                
            if constraint_value[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(0.25) > optimal_slack_value[constraint_counter]:
                temp_list_p25.append(constraint_names[constraint_counter])
                
            if constraint_value[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(0.5) > optimal_slack_value[constraint_counter]:
                temp_list_p50.append(constraint_names[constraint_counter])
                
            if constraint_value[constraint_counter][variable_counter]*optimal_variable_value[variable_counter]*(1) > optimal_slack_value[constraint_counter]:
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
    
    col_var_changes = ['Optimal Solution - 1', 
                       'Optimal Solution', 
                       'Optimal Solution + 1', 
                       spacing, 
                       'Optimal Solution - 100%', 
                       'Optimal Solution - 50%', 
                       'Optimal Solution - 25%', 
                       'Optimal Solution - 10%', 
                       'Optimal Solution', 
                       'Optimal Solution + 10%', 
                       'Optimal Solution + 25%', 
                       'Optimal Solution + 50%', 
                       'Optimal Solution + 100%']
    
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
        
        table_var_changes.iloc[fill_counter+1,:] = [optimal_variable_value[int(fill_counter/4)]-1, 
                                                    optimal_variable_value[int(fill_counter/4)], 
                                                    optimal_variable_value[int(fill_counter/4)]+1, 
                                                    spacing, 
                                                    0, 
                                                    optimal_variable_value[int(fill_counter/4)]*0.5, 
                                                    optimal_variable_value[int(fill_counter/4)]*0.75, 
                                                    optimal_variable_value[int(fill_counter/4)]*0.9, 
                                                    optimal_variable_value[int(fill_counter/4)], 
                                                    optimal_variable_value[int(fill_counter/4)]*1.1, 
                                                    optimal_variable_value[int(fill_counter/4)]*1.25, 
                                                    optimal_variable_value[int(fill_counter/4)]*1.5, 
                                                    optimal_variable_value[int(fill_counter/4)]*2] 
        
        table_var_changes.iloc[fill_counter+2,:] = [optimal_objective_value-obj_coef[int(fill_counter/4)], 
                                                    optimal_objective_value, 
                                                    optimal_objective_value+obj_coef[int(fill_counter/4)], 
                                                    spacing, 
                                                    optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(-1), 
                                                    optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(-0.5), 
                                                    optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(-0.25), 
                                                    optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(-0.1), 
                                                    optimal_objective_value, 
                                                    optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(0.1), 
                                                    optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(0.25), 
                                                    optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(0.5), 
                                                    optimal_objective_value-obj_coef[int(fill_counter/4)]*optimal_variable_value[int(fill_counter/4)]*(1)]
        
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
    
    global table_obj_coef
    
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
        Simplex()
        obj_minus = optimal_solution_Simplex[0]
        
        if NoFeasibleSolution == True:
            new_optimal_minus.append('INFESIBLE')
        else:
            new_optimal_minus.append(obj_minus)
            
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] += 1
        Simplex()
        obj_plus = optimal_solution_Simplex[0]
        
        if NoFeasibleSolution == True:
            new_optimal_plus.append('INFESIBLE')
        else:
            new_optimal_plus.append(obj_plus)
        
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = 0
        Simplex() 
        obj_m100 = optimal_solution_Simplex[0]  
        
        if NoFeasibleSolution == True:
            new_optimal_m100.append('INFESIBLE')
        else:
            new_optimal_m100.append(obj_m100)
        
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*0.5
        Simplex() 
        obj_m50 = optimal_solution_Simplex[0]  
        
        if NoFeasibleSolution == True:
            new_optimal_m50.append('INFESIBLE')
        else:
            new_optimal_m50.append(obj_m50)

        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*0.75
        Simplex()
        obj_m25 = optimal_solution_Simplex[0] 
        
        if NoFeasibleSolution == True:
            new_optimal_m25.append('INFESIBLE')
        else:
            new_optimal_m25.append(obj_m25)    
            
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*0.9
        Simplex() 
        obj_m10 = optimal_solution_Simplex[0]  
        
        if NoFeasibleSolution == True:
            new_optimal_m10.append('INFESIBLE')
        else:
            new_optimal_m10.append(obj_m10)
            
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*1.1
        Simplex() 
        obj_p10 = optimal_solution_Simplex[0]   
        
        if NoFeasibleSolution == True:
            new_optimal_p10.append('INFESIBLE')
        else:
            new_optimal_p10.append(obj_p10)
        
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*1.25
        Simplex() 
        obj_p25 = optimal_solution_Simplex[0]     
        
        if NoFeasibleSolution == True:
            new_optimal_p25.append('INFESIBLE')
        else:
            new_optimal_p25.append(obj_p25)

        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*1.5
        Simplex()
        obj_p50 = optimal_solution_Simplex[0]      
        
        if NoFeasibleSolution == True:
            new_optimal_p50.append('INFESIBLE')
        else:
            new_optimal_p50.append(obj_p50)
            
        #
        
        obj_coef = copy.deepcopy(original_obj_coef)
        obj_coef[coef_counter] = obj_coef[coef_counter]*2
        Simplex()
        obj_p100 = optimal_solution_Simplex[0]  
        
        if NoFeasibleSolution == True:
            new_optimal_p100.append('INFESIBLE')
        else:
            new_optimal_p100.append(obj_p100) 
        
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
        
        table_obj_coef.iloc[fill_counter+1,:] = [original_obj_coef[int(fill_counter/4)]-1, 
                                                 original_obj_coef[int(fill_counter/4)], 
                                                 original_obj_coef[int(fill_counter/4)]+1, 
                                                 spacing, 
                                                 0, 
                                                 original_obj_coef[int(fill_counter/4)]*0.5, 
                                                 original_obj_coef[int(fill_counter/4)]*0.75, 
                                                 original_obj_coef[int(fill_counter/4)]*0.9, 
                                                 original_obj_coef[int(fill_counter/4)], 
                                                 original_obj_coef[int(fill_counter/4)]*1.1, 
                                                 original_obj_coef[int(fill_counter/4)]*1.25, 
                                                 original_obj_coef[int(fill_counter/4)]*1.5, 
                                                 original_obj_coef[int(fill_counter/4)]*2] 
        
        table_obj_coef.iloc[fill_counter+2,:] = [new_optimal_minus[int(fill_counter/4)], 
                                                 original_optimal_solution[0], 
                                                 new_optimal_plus[int(fill_counter/4)], 
                                                 spacing, 
                                                 new_optimal_m100[int(fill_counter/4)], 
                                                 new_optimal_m50[int(fill_counter/4)], 
                                                 new_optimal_m25[int(fill_counter/4)], 
                                                 new_optimal_m10[int(fill_counter/4)], 
                                                 original_optimal_solution[0], 
                                                 new_optimal_p10[int(fill_counter/4)], 
                                                 new_optimal_p25[int(fill_counter/4)], 
                                                 new_optimal_p50[int(fill_counter/4)], 
                                                 new_optimal_p100[int(fill_counter/4)]]
        
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


def Con_Bound(bound, constraint_names, optimal_solution_Simplex): 
    
    global table_bound
    
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
        Simplex()  
        bound_minus = optimal_solution_Simplex[0] 
        
        if NoFeasibleSolution == True:
            new_optimal_minus.append('INFESIBLE')
        else:
            new_optimal_minus.append(bound_minus)
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] += 1
        Simplex()  
        bound_plus = optimal_solution_Simplex[0] 
        
        if NoFeasibleSolution == True:
            new_optimal_plus.append('INFESIBLE')
        else:
            new_optimal_plus.append(bound_plus)
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = 0
        Simplex() 
        bound_m100 = optimal_solution_Simplex[0]   
        
        if NoFeasibleSolution == True:
            new_optimal_m100.append('INFESIBLE')
        else:
            new_optimal_m100.append(bound_m100)
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*0.5
        Simplex() 
        bound_m50 = optimal_solution_Simplex[0]   
        
        if NoFeasibleSolution == True:
            new_optimal_m50.append('INFESIBLE')
        else:
            new_optimal_m50.append(bound_m50)

        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*0.75
        Simplex()
        bound_m25 = optimal_solution_Simplex[0]    
        
        if NoFeasibleSolution == True:
            new_optimal_m25.append('INFESIBLE')
        else:
            new_optimal_m25.append(bound_m25)    
            
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*0.9
        Simplex()
        bound_m10 = optimal_solution_Simplex[0]  
        
        if NoFeasibleSolution == True:
            new_optimal_m10.append('INFESIBLE')
        else:
            new_optimal_m10.append(bound_m10)
            
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*1.1
        Simplex()
        bound_p10 = optimal_solution_Simplex[0]   
        
        if NoFeasibleSolution == True:
            new_optimal_p10.append('INFESIBLE')
        else:
            new_optimal_p10.append(bound_p10)
        
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*1.25
        Simplex()
        bound_p25 = optimal_solution_Simplex[0]  
        
        if NoFeasibleSolution == True:
            new_optimal_p25.append('INFESIBLE')
        else:
            new_optimal_p25.append(bound_p25)

        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*1.5
        Simplex()
        bound_p50 = optimal_solution_Simplex[0]     
        
        if NoFeasibleSolution == True:
            new_optimal_p50.append('INFESIBLE')
        else:
            new_optimal_p50.append(bound_p50)
            
        #
        
        bound = copy.deepcopy(original_con_bound)
        bound[bound_counter] = bound[bound_counter]*2
        Simplex()
        bound_p100 = optimal_solution_Simplex[0]   
        
        if NoFeasibleSolution == True:
            new_optimal_p100.append('INFESIBLE')
        else:
            new_optimal_p100.append(bound_p100)   
               
        #
        
        bound_counter += 1
    
    spacing = '...'
    
    col_bound = ['Bound Value - 1', 
                 'Bound Value', 
                 'Bound Value + 1', 
                 spacing, 
                 'Bound Value - 100%', 
                 'Bound Value - 50%', 
                 'Bound Value - 25%', 
                 'Bound Value - 10%', 
                 'Bound Value', 
                 'Bound Value + 10%', 
                 'Bound Value + 25%', 
                 'Bound Value + 50%', 
                 'Bound Value + 100%']
    
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
        
        table_bound.iloc[fill_counter+1,:] = [original_con_bound[int(fill_counter/4)]-1, 
                                              original_con_bound[int(fill_counter/4)], 
                                              original_con_bound[int(fill_counter/4)]+1, 
                                              spacing, 
                                              0, 
                                              original_con_bound[int(fill_counter/4)]*0.5, 
                                              original_con_bound[int(fill_counter/4)]*0.75, 
                                              original_con_bound[int(fill_counter/4)]*0.9, 
                                              original_con_bound[int(fill_counter/4)], 
                                              original_con_bound[int(fill_counter/4)]*1.1, 
                                              original_con_bound[int(fill_counter/4)]*1.25, 
                                              original_con_bound[int(fill_counter/4)]*1.5, 
                                              original_con_bound[int(fill_counter/4)]*2]
        
        table_bound.iloc[fill_counter+2,:] = [new_optimal_minus[int(fill_counter/4)], 
                                              original_optimal_solution[0], 
                                              new_optimal_plus[int(fill_counter/4)], 
                                              spacing, 
                                              new_optimal_m100[int(fill_counter/4)], 
                                              new_optimal_m50[int(fill_counter/4)], 
                                              new_optimal_m25[int(fill_counter/4)], 
                                              new_optimal_m10[int(fill_counter/4)], 
                                              original_optimal_solution[0], 
                                              new_optimal_p10[int(fill_counter/4)], 
                                              new_optimal_p25[int(fill_counter/4)], 
                                              new_optimal_p50[int(fill_counter/4)], 
                                              new_optimal_p100[int(fill_counter/4)]]
        
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

def Con_Remove(constraint_names, constraint, constraint_type, bound, optimal_solution_Simplex):
    
    global table_con_remove
    
    original_optimal_solution = copy.deepcopy(optimal_solution_Simplex[:])
    constraint_value = copy.deepcopy(Deep_Copy_constraint[1])
    
    original_constraint_names = copy.deepcopy(constraint_names[:])
    original_constraint = copy.deepcopy(constraint_value[:])
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
            constraint_value = copy.deepcopy(original_constraint)
            bound = copy.deepcopy(original_bound)
            
            del constraint_names[soft_con_remove_counter]
            del constraint_value[soft_con_remove_counter]
            del bound[soft_con_remove_counter]
            
            Simplex()
            Simplex_excl_soft = optimal_solution_Simplex[0]
            
            if NoFeasibleSolution == True:
                optimal_excl_soft.append('INFESIBLE')
            else:            
                optimal_excl_soft.append(Simplex_excl_soft)
        
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
    
    # print sensitivity analysis in a frame
    
    def print_frame(*words):
        
        size = max(len(word) for word in words)
        print('\033[1m' + '=' * (size + 6))
        
        for word in words:
            print('\033[1m' + '== {w:<{s}} =='.format(w=word, s=size))
            
        print('\033[1m' + '=' * (size + 6))
    
    print_frame("Sensitivity", "Analysis", "for: ", obj_names[0])
    
    
    # then run all the function to change parameters, from which explanations are extracted
    
    # change optimal solution for each variable
    
    SA_Opt_Var = Optimal_Var(optimal_solution_Simplex)
    display(SA_Opt_Var)
    
    print('\nThe table above shows that the best value for ' + str(obj_names[0]) + ' is ' + str(SA_Opt_Var.iloc[2,1]) + ', under the optimal solution, ')
    print('when the ' + str(len(variable_names)) + ' variables: ' + str(variable_names[:]) + ' , are set to: ')
    
    var_values_counter = 0
    for var_values_counter in range(len(variable_names)):
        print(str(variable_names[var_values_counter]) + ' = ' + str(SA_Opt_Var.iloc[var_values_counter*4 + 1, 1]) + ' , ')
        var_values_counter += 1
    print('respectively.\n')
    
    print('If variables are set to other values, the objective value ' + str(obj_names[0]) + ' will be either inferior than ' + str(SA_Opt_Var.iloc[2,1]) + ' , or violating constraints! \n')
    print('The following graphs have shown the impacts on the objective value by changing the optimal vaiables value: \n')
    print('(Notes: Blue points are feasible, while Red points are violating at least one constraints)\n')
    
    # plot the objective value against changes in each variable
    
    plot_counter = 0
    
    for plot_counter in range(len(variable_names)):
         
        x_b = []
        y_b = []
        x_r = []
        y_r = []
        
        color_counter = 0
        
        # check if constraints are violated, if yes plot red, otherwise plot blue
        
        for color_counter in range(SA_Opt_Var.shape[1]):
            if isinstance(SA_Opt_Var.iloc[plot_counter*4 + 1, color_counter], int) == True or isinstance(SA_Opt_Var.iloc[plot_counter*4 + 1, color_counter], float) == True:
                if isinstance(SA_Opt_Var.iloc[plot_counter*4 + 2, color_counter], int) == True or isinstance(SA_Opt_Var.iloc[plot_counter*4 + 2, color_counter], float) == True:
                    if SA_Opt_Var.iloc[plot_counter*4 + 3, color_counter] == None:
                        x_b.append(SA_Opt_Var.iloc[plot_counter*4 + 1, color_counter])
                        y_b.append(SA_Opt_Var.iloc[plot_counter*4 + 2, color_counter])
                    else:
                        x_r.append(SA_Opt_Var.iloc[plot_counter*4 + 1, color_counter])
                        y_r.append(SA_Opt_Var.iloc[plot_counter*4 + 2, color_counter])

            color_counter += 1  
            
        plt.plot(x_b, y_b, 'bo')
        plt.plot(x_r, y_r, 'ro')

        plt.title('Objective Value Changes in Different ' + str(variable_names[plot_counter]))
        plt.xlabel('Value of ' + str(variable_names[plot_counter]))
        plt.ylabel('Objective Value of ' + str(obj_names[0]))
        plt.show()
        
        plt.clf()
        plt.cla()
        plt.close()
        
        plot_counter += 1
    
    
    print('\n==================================================\n')
    
    
    # change coefficients in objective function   
    
    SA_Obj_Coe = Obj_Coef(obj_coef, optimal_solution_Simplex)
    display(SA_Obj_Coe)
    
    # return table_obj_coef
    
    print('\nThe table above shows that the best value for ' + str(obj_names[0]) + ' is ' + str(SA_Obj_Coe.iloc[2,1]) + ', under the optimal solution, ')
    print('when the coefficients of ' + str(len(variable_names)) + ' variables: ' + str(variable_names[:]) + ' , are set to: ')
    
    obj_coe_counter = 0
    row_name_list = list(SA_Obj_Coe.index)
    for obj_coe_counter in range(len(variable_names)):
        print(str(row_name_list[obj_coe_counter*4 + 1]) + ' = ' + str(SA_Obj_Coe.iloc[obj_coe_counter*4 + 1, 1]) + ' , ')
        obj_coe_counter += 1
    print('respectively.\n')
    
    print('If coefficients are set to other values, the objective value ' + str(obj_names[0]) + ' might be changed and different from ' + str(SA_Obj_Coe.iloc[2,1]) + ' , or even infeasible.\n')
    print('The following graphs have shown the impacts on the objective value by changing the coefficient of each variable: \n')
    
    # plot the objective value against changes in the coefficient of each variable
    
    plot_counter = 0
    
    for plot_counter in range(len(variable_names)):
         
        x_k = []
        y_k = []
        
        col_counter = 0
        
        for col_counter in range(SA_Obj_Coe.shape[1]):
            if isinstance(SA_Obj_Coe.iloc[plot_counter*4 + 1, col_counter], int) == True or isinstance(SA_Obj_Coe.iloc[plot_counter*4 + 1, col_counter], float) == True:
                if isinstance(SA_Obj_Coe.iloc[plot_counter*4 + 2, col_counter], int) == True or isinstance(SA_Obj_Coe.iloc[plot_counter*4 + 2, col_counter], float) == True:
                    x_k.append(SA_Obj_Coe.iloc[plot_counter*4 + 1, col_counter])
                    y_k.append(SA_Obj_Coe.iloc[plot_counter*4 + 2, col_counter])

            color_counter += 1  
            
        plt.plot(x_k, y_k, 'ko')

        plt.title('Objective Value Changes in Different Coefficients of ' + str(variable_names[plot_counter]))
        plt.xlabel('Coefficient of ' + str(variable_names[plot_counter]))
        plt.ylabel('Objective Value of ' + str(obj_names[0]))
        plt.show()
        
        plt.clf()
        plt.cla()
        plt.close()
        
        plot_counter += 1
    
    
    print('\n==================================================\n')
    
    
    # change bound value of each constraint
    
    SA_Con_Bou = Con_Bound(bound, constraint_names, optimal_solution_Simplex)
    display(SA_Con_Bou)
    
    # return table_bound
    
    print('\nThe table above shows that the best value for ' + str(obj_names[0]) + ' is ' + str(SA_Con_Bou.iloc[2,1]) + ', under the optimal solution, ')
    print('when the constraint bound of ' + str(len(constraint_names)) + ' constraints: ' + str(constraint_names[:]) + ' , are set to: ')
    
    con_bou_counter = 0
    row_name_list = list(SA_Con_Bou.index)
    for con_bou_counter in range(len(constraint_names)):
        print(str(row_name_list[con_bou_counter*4 + 1]) + ' = ' + str(SA_Con_Bou.iloc[con_bou_counter*4 + 1, 1]) + ' , ')
        con_bou_counter += 1
    print('respectively.\n')
    
    print('If bounds are set to other values, the objective value ' + str(obj_names[0]) + ' might be changed and different from ' + str(SA_Con_Bou.iloc[2,1]) + ' .\n')
    
    print('The slack value shows that how much each constraint can be changed before it will be violated.\n')
    slack_optimal_solution = copy.deepcopy(optimal_solution_Simplex[2])
    print('The slack value for constraints ' + str(constraint_names[:]) + ' are ' + str(slack_optimal_solution[:]) + ' , respectively.\n')
    print('Meaning that: \n')
    slack_counter = 0
    for slack_counter in range(len(constraint_names)):
        if slack_optimal_solution[slack_counter] == 0:
            print('No changes should be made in the constraint ' + str(constraint_names[slack_counter]) + ' , otherwise the constraint will be violated, and optimal solution might change as well;\n')
        else:
            print('The changes in the constraint ' + str(constraint_names[slack_counter]) + ' should not be exceeding ' + str(slack_optimal_solution[slack_counter]) + ' , otherwise the constraint will be violated, and optimal solution might change as well;\n')
        slack_counter += 1
    
    print('\nThe following graphs have shown the impacts on the objective value by changing the bound for each constraint: \n')
    
    # plot the objective value against changes in each bound
    
    plot_counter = 0
    
    for plot_counter in range(len(constraint_names)):
         
        x_g = []
        y_g = []
        
        col_counter = 0
        
        for col_counter in range(SA_Con_Bou.shape[1]):
            if isinstance(SA_Con_Bou.iloc[plot_counter*4 + 1, col_counter], int) == True or isinstance(SA_Con_Bou.iloc[plot_counter*4 + 1, col_counter], float) == True:
                if isinstance(SA_Con_Bou.iloc[plot_counter*4 + 2, col_counter], int) == True or isinstance(SA_Con_Bou.iloc[plot_counter*4 + 2, col_counter], float) == True:
                    x_g.append(SA_Con_Bou.iloc[plot_counter*4 + 1, col_counter])
                    y_g.append(SA_Con_Bou.iloc[plot_counter*4 + 2, col_counter])

            color_counter += 1  
            
        plt.plot(x_g, y_g, 'go')

        plt.title('Objective Value Changes in Different Bound of ' + str(constraint_names[plot_counter]))
        plt.xlabel('Bound of ' + str(constraint_names[plot_counter]))
        plt.ylabel('Objective Value of ' + str(obj_names[0]))
        plt.show()
        
        plt.clf()
        plt.cla()
        plt.close()
        
        plot_counter += 1
    
    
    print('\n==================================================\n')
   
    
    # remove soft constraints
    
    SA_Con_Rem = Con_Remove(constraint_names, constraint, constraint_type, bound, optimal_solution_Simplex)
    
    # return table_con_remove, None if there is no soft constraints
    
    try:
        shape_checker = SA_Con_Rem.shape[0]
        display(SA_Con_Rem)
        
        soft_cons_index = [ind for ind, soft in enumerate(constraint_type) if soft == 'soft']
        soft_cons = [constraint_names[name_ind] for name_ind in soft_cons_index]
        print('\nThe table above shows the changes in the value of objective ' + str(obj_names[0]) + ' , if soft constraints ' + str(soft_cons_index) + ' are removed.\n')
        
        exp_counter = 0
        
        for exp_counter in range(len(soft_cons_index)):
            if SA_Con_Rem.iloc[exp_counter*4 + 2, 1] == 'INFEASIBLE':
                print('If soft constraint ' + str(soft_cons[exp_counter]) + ' is removed, the objective value ' + str(obj_names[0]) + ' will become infeasible.\n')
            elif SA_Con_Rem.iloc[exp_counter*4 + 3, 1] == 0:
                print('If soft constraint ' + str(soft_cons[exp_counter]) + ' is removed, the objective value ' + str(obj_names[0]) + ' is unchanged.\n')
            else:
                print('If soft constraint ' + str(soft_cons[exp_counter]) + ' is removed, the objective value ' + str(obj_names[0]) + ' is changed to ' + str(SA_Con_Rem.iloc[exp_counter*4 + 2, 1]) + ' .\n')
        
    except AttributeError:
        print('There are no soft constraints to be removed.\n')
    
    
    print_frame("The", "End", "of", "Sensitivity", "Analysis")    
    
    
Sensitivity_Analysis()



# The End of Sensitivity Analysis Module
