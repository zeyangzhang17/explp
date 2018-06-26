
def constraint(Constraint_Name=[], Constraint_Coefficient=[], Bound_Name=[], Bound_Value=[], Maximise=False, Type=[]):
    
    
    len_con_name = len(Constraint_Name)
    len_con_coef = len(Constraint_Coefficient)

    len_counter = 0

    for len_counter in range(len_con_coef):
        if len(Constraint_Coefficient[len_counter]) != len_con_name:
            print('Error! The Length of Constraint Name and Constraint Coefficient DO NOT Match!')
            break
        else:
            len_counter += 1
    
    if Maximise == False:
        constraint = Constraint_Coefficient
        bound = Bound_Value
    else:
        constraint = -Constraint_Coefficient
        bound = -Bound_Value   
    
    constraint_names = Constraint_Name
    bound_names = Bound_Name
    constraint_type = Type
    
    return constraint_names, constraint, bound_names, bound, constraint_type

