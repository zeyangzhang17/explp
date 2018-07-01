
def integer_constraint(Integer_Variable_Name = []):
    
    if set(Integer_Variable_Name).issubset(obj_names) == False:
        print('Error! The Integer Variable Name DOES NOT Match with Variable Name in Objectives')
    
    return Integer_Variable_Name 
