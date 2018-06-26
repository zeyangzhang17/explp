
# coding: utf-8

def Simplex():
    
    var_count = len(variable_names)
    con_count = len(constraint_names)
    
    obj_coef_df = [1] + obj_coef
    objective_dataframe = {obj_names[0]:obj_coef_df}

    objective_index = obj_names + variable_names
    
    constraint_dataframe = {}
    counter_constraint = 0

    for counter_constriant in range(con_count):
        constraint_dataframe.update({constraint_names[counter_constriant]:constraint[counter_constriant]})
        counter_constraint += 1
        
    slack_var = np.identity(con_count)

    slack_var_names = []
    counter_names = 0
    
    for counter_names in range(len(constraint)):
        slack_var_names.append('slack_' + str(constraint_names[counter_names]))
        counter_names += 1
        
    DF_objective = pd.DataFrame(data=objective_dataframe, index=objective_index).T

    DF_constraint = pd.DataFrame(data=constraint_dataframe, index=variable_names).T

    DF_slack_var = pd.DataFrame(data=slack_var, columns=slack_var_names, index=constraint_names)

    DF_bound = pd.DataFrame(data=bound, columns=bound_names, index=constraint_names)
    
    tableau_no_obj = pd.concat([DF_constraint, DF_slack_var, DF_bound], axis=1)
    
    tableau = pd.concat([DF_objective, tableau_no_obj]).fillna(0)
    tableau = tableau[objective_index + slack_var_names + bound_names]
    
    # BFS = {'Variables Value':[0] * var_count, 'Slack Variables Value':bound, 'Objective Value':[0]}
    
    
    pivoting = tableau.copy()
    
    pivoting_col_list = list(pivoting)
    
    times_counter = 0
    
    while any(pivoting.iloc[0,1:var_count+con_count+1].values>0) == True:
        
        times_counter += 1
    
        pivot_column = pivoting.iloc[0,1:var_count+con_count+1].values.tolist().index(max(pivoting.iloc[0,1:var_count+con_count+1])) + 1
        
        test_ratios = []
        pt_i = 1

        for pt_i in range(1,con_count+1):
            test_ratios.append(pivoting[bound_names[0]][pt_i]/pivoting[pivoting_col_list[pivot_column]][pt_i])
            pt_i += 1
            
        pivot_row = test_ratios.index(min(test_ratios))+1
        
        pivot_value = pivoting.iloc[pivot_row, pivot_column]
        
        pivoting.iloc[pivot_row,:] = pivoting.iloc[pivot_row,:] / pivot_value
        
        pi_count = 0
        
        for pi_count in range(con_count+1):
            if pi_count != pivot_row:
                pivoting.iloc[pi_count,:] = pivoting.iloc[pi_count,:] - pivoting.iloc[pi_count, pivot_column] * pivoting.iloc[pivot_row,:]
                pi_count += 1
            else:
                continue
        
        if times_counter >= 1000:
            print('Error! Too Many Iterations!')
            break
        else:
            continue
    
    var_optimal = -pivoting.iloc[0,1:var_count+1]
    slack_optimal = -pivoting.iloc[0,var_count+1:var_count+con_count+1]
    obj_optimal = -pivoting.iloc[0,-1] / pivoting.iloc[0,0]
    
    optimal_solution_Simplex = {'Variables Value': var_optimal, 'Slack Variables Value': slack_optimal, 'Objective Value': obj_optimal}
            
    return optimal_solution_Simplex
        