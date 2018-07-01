
def objective(Objective_Name=[], Variable_Name=[], Variable_Coefficient=[], Maximise=True):
    
    if len(Objective_Name) != 1:
        print('Error! Please Enter ONE and ONLY ONE Objective Name.\nFor Multi-Objective Problems, Please Use multi_objective() Function.\n')
    else:
        print('\n')
        
        
    len_var_name = len(Variable_Name)
    len_var_coef = len(Variable_Coefficient)

    len_counter = 0

    for len_counter in range(len_var_coef):
        if len(Variable_Coefficient[len_counter]) != len_var_name:
            print('Error! The Length of Variable Name and Variable Coefficient DO NOT Match!')
            break
        else:
            len_counter += 1
    
    if Maximise == True:
        obj_coef = Variable_Coefficient
    else:
        obj_coef = -Variable_Coefficient
    
    obj_names = Objective_Name 
    variable_names = Variable_Name
    
    return obj_names, obj_coef, variable_names
