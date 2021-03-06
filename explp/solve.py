# Module: solve

# Functions: 
    # solve.Simplex()
    # solve.Branch_And_Bound()
    # solve.Solve()

    
    
# Last Updated: 10th August 2018



import math
import pandas as pd
import numpy as np
import copy


def Simplex():
    
    global tableau, optimal_solution_Simplex, NoFeasibleSolution
    
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
        constraint_value = copy.deepcopy(Deep_Copy_constraint[1])
        constraint_dataframe.update({constraint_names[counter_constriant]:constraint_value[counter_constriant]})
        counter_constraint += 1
    
    # introduce slack variables
    
    slack_var = np.identity(con_count)

    slack_var_names = []
    counter_names = 0
    
    # name the slack variables
    
    for counter_names in range(len(constraint_value)):
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
    
    pivoting = copy.deepcopy(tableau)
    
    pivoting_col_list = list(pivoting)
    
    # add a time counter for the times of iterating
    
    times_counter = 0
    pivot_column_record = []
    pivot_row_record = []
    NoFeasibleSolution = False
    
    # if any reduced costs (negative of objective coefficients) are negative:
    
    while any(pivoting.iloc[0,1:var_count+con_count+1].values<0) == True:
        
        times_counter += 1
    
        # choose pivot column: the most negative value of reduced costs
        
        # find the most negative value
        
        if times_counter <= var_count+con_count:
            pivot_column = pivoting.iloc[0,1:var_count+con_count+1].values.tolist().index(min(pivoting.iloc[0,1:var_count+con_count+1])) + 1
            
        # if cycling, use Bland's rule to find the first negative value
        
        else:
            pivot_list_cyc = pivoting.iloc[0,1:var_count+var_count+1].values.tolist()
            list_cyc_counter = 0
            for list_cyc_counter in range(len(pivot_list_cyc)):
                if pivot_list_cyc[list_cyc_counter] < 0:
                    first_negative_index = list_cyc_counter
                    break
                else:
                    list_cyc_counter += 1
            
            pivot_column = first_negative_index + 1
            
            # reset time counter to 0
            
            times_counter = 0
        
        pivot_column_record.append(pivot_column)
        
        # compute test ratio (bound / pivot column) and select the smallest
        
        test_ratios = []
        pt_i = 1

        for pt_i in range(1,con_count+1):
            try:
                ratio = pivoting.iloc[pt_i,0] / pivoting.iloc[pt_i,pivot_column]
            except ZeroDivisionError:
                ratio = 0
                
            if pivoting.iloc[pt_i,0] <= 0 and pivoting.iloc[pt_i,pivot_column] <= 0:
                ratio = 0
            test_ratios.append(ratio)
            pt_i += 1
        
        if all(ratio <= 0 for ratio in test_ratios) == True:
            NoFeasibleSolution = True
            UnBounded = True
            print('Error! The Problem is UN-BOUNDED !')
            break
        else:
            UnBounded = False
        
        pivot_row = test_ratios.index(min([ratio for ratio in test_ratios if ratio > 0]))+1
        pivot_row_record.append(pivot_row)
        
        pivot_value = pivoting.iloc[pivot_row, pivot_column]
        
        # set pivot value to 1 by dividing the pivot row by pivot value, for further computing
        
        pivoting.iloc[pivot_row,:] = pivoting.iloc[pivot_row,:] / pivot_value
        
        # elementary row operations
        
        pi_count = 0
        
        for pi_count in range(con_count+1):
            if pi_count != pivot_row:
                pivoting.iloc[pi_count,:] = pivoting.iloc[pi_count,:] - pivoting.iloc[pivot_row,:] * pivoting.iloc[pi_count, pivot_column] 
            else:
                continue
                
            pi_count += 1
            
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
        if pivot_column_record[var_counter] <= len(variable_names):
            var_optimal[pivot_column_record[var_counter]-1] = pivoting.iloc[pivot_row_record[var_counter],0]
        else:
            slack_optimal[pivot_column_record[var_counter]-1-len(variable_names)] = pivoting.iloc[pivot_row_record[var_counter],0]
        var_counter += 1
    
    # in case multiple variables are assigned to the same row value, wipe the former values to 0
    
    repeat_counter = 0
    
    for repeat_counter in range(len(pivot_row_record)):
        if pivot_row_record[repeat_counter] in pivot_row_record[repeat_counter+1:]:
            if pivot_row_record[repeat_counter] <= len(variable_names):
                var_optimal[pivot_row_record[repeat_counter]-1] = 0
            else:
                slack_optimal[pivot_row_record[repeat_counter]-1] = 0
                
        repeat_counter += 1
    
    optimal_solution_Simplex = copy.deepcopy([obj_optimal, var_optimal, slack_optimal])
    
    if NoFeasibleSolution == True:
        
        print('\nThere is NO Feasible Solutions!\n')
        
        if UnBounded == True:
            print('There is a high probability that constraints are unbounded!\n')
            print('Please check for the constraints.\n')
        else:
            print('There is a high probability that constraints are contradicting with each other!\n')
            print('Please check for the constraints.\n')



# Branch_And_Bound Function:

def Branch_And_Bound(optimal_solution_Simplex):
    
    global optimal_solution_Branch_and_Bound, NoFeasibleSolution
    global Floor_NoFS, Floor_optimal_solution_Simplex
    global Ceiling_NoFS, Ceiling_optimal_solution_Simplex
    
    
    # firstly do relaxation of all integer constraints 
    # i.e. to use Simplex algorithm to find global optimal as upper bound
    
    # Non integer-constrained solution -- objective value and variable coefficient
    
    non_int_con_sol_obj = copy.deepcopy(optimal_solution_Simplex[0])
    non_int_con_sol_var = copy.deepcopy(optimal_solution_Simplex[1])
    non_int_con_sol_slack = copy.deepcopy(optimal_solution_Simplex[2])

    # record all interger constrained variables
    
    int_con_sol_var = []
    
    for integer_index in Integer_Index:
        int_con_sol_var.append(optimal_solution_Simplex[1][integer_index])
        
    # check if all required integer constraint is satisfied
        
    def list_int_checker(List):
        
        global all_int, int_counter
    
        # check if all items in the list are met with integer constraints
    
        int_list = [int(x) for x in List]
        
        int_counter = 0
    
        for int_counter in range(len(List)):
            
            # check if all integer constraints are met
            
            if int_list[int_counter] == List[int_counter]:
                all_int = True
                int_counter +=1
                
            # if not, return the index of the first non-integer
            
            else:
                all_int = False
                break
            
 
    list_int_checker(int_con_sol_var)
    
    runtime_counter = 0

    
    while all_int == False:
        
        # use the first non-integer and compute floor and ceiling
        
        bnb_var_index = copy.deepcopy(Integer_Index[int_counter])
        bnb_var = copy.deepcopy(optimal_solution_Simplex[1][bnb_var_index])
        floor_bnb = np.floor(bnb_var)
        ceil_bnb = np.ceil(bnb_var)
        
        pivoting_floor = copy.deepcopy(tableau)
        pivoting_ceiling = copy.deepcopy(tableau)
        
        
        # Branch 1: Floor
                
        # take the targetted non-integer variable out of objectives and constraints
        
        pivoting_floor.iloc[:,0] -= pivoting_floor.iloc[:,bnb_var_index+1] * (pivoting_floor.iloc[0,bnb_var_index+1] * floor_bnb)
        pivoting_floor.drop([variable_names[bnb_var_index]], axis = 1)
        pivoting = copy.deepcopy(pivoting_floor)
        
        # Then run the same steps as Simplex function
        
        var_count = len(variable_names)-1
        con_count = len(constraint_names)
        
        pivoting_col_list = list(pivoting)
        times_counter = 0
        pivot_column_record = []
        pivot_row_record = []
        NoFeasibleSolution = False

        while any(pivoting.iloc[0,1:var_count+con_count+1].values<0) == True:
            times_counter += 1
        
            if times_counter <= var_count+con_count:
                pivot_column = pivoting.iloc[0,1:var_count+con_count+1].values.tolist().index(min(pivoting.iloc[0,1:var_count+con_count+1])) + 1

            else:
                pivot_list_cyc = pivoting.iloc[0,1:var_count+con_count+1].values.tolist()
                list_cyc_counter = 0
                for list_cyc_counter in range(len(pivot_list_cyc)):
                    if pivot_list_cyc[list_cyc_counter] < 0:
                        first_negative_index = list_cyc_counter
                        break
                    else:
                        list_cyc_counter += 1

                pivot_column = first_negative_index + 1
            
                # reset time counter to 0

                times_counter = 0

            pivot_column_record.append(pivot_column)
            
            test_ratios = []
            pt_i = 1

            for pt_i in range(1,con_count+1):
                try:
                    ratio = pivoting.iloc[pt_i,0] / pivoting.iloc[pt_i,pivot_column]
                except ZeroDivisionError:
                    ratio = 0

                if pivoting.iloc[pt_i,0] <= 0 and pivoting.iloc[pt_i,pivot_column] <= 0:
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
            pivoting.iloc[pivot_row,:] = pivoting.iloc[pivot_row,:] / pivot_value
            pi_count = 0
            
            for pi_count in range(con_count+1):
                if pi_count != pivot_row:
                    pivoting.iloc[pi_count,:] = pivoting.iloc[pi_count,:] - pivoting.iloc[pi_count, pivot_column] * pivoting.iloc[pivot_row,:]
                else:
                    continue
                    
                pi_count += 1

        obj_optimal = pivoting.iloc[0,0]
        slack_optimal = pivoting.iloc[1:,0].tolist()
        slack_counter = 0

        for slack_counter in range(len(pivot_row_record)):
            slack_optimal[pivot_row_record[slack_counter]-1] = 0
            slack_counter += 1

        var_optimal = [0] * var_count

        var_counter = 0

        for var_counter in range(len(pivot_row_record)):
            if pivot_column_record[var_counter] <= len(variable_names)-1:
                var_optimal[pivot_column_record[var_counter]-1] = pivoting.iloc[pivot_row_record[var_counter],0]
            else:
                slack_optimal[pivot_column_record[var_counter]-1-var_count] = pivoting.iloc[pivot_row_record[var_counter],0]
            var_counter += 1

        # in case multiple variables are assigned to the same row value, wipe the former values to 0

        repeat_counter = 0

        for repeat_counter in range(len(pivot_row_record)):
            if pivot_row_record[repeat_counter] in pivot_row_record[repeat_counter+1:]:
                if pivot_row_record[repeat_counter] <= len(variable_names)-1:
                    var_optimal[pivot_row_record[repeat_counter]-1] = 0
                else:
                    slack_optimal[pivot_row_record[repeat_counter]-1] = 0

            repeat_counter += 1
    
            
        # add back fixed variable (floor value) to the optimal solution
        
        var_optimal += [floor_bnb]
        var_optimal.insert(bnb_var_index, var_optimal.pop())
        
        Floor_optimal_solution_Simplex = copy.deepcopy([obj_optimal, var_optimal, slack_optimal])
        Floor_NoFS = copy.deepcopy(NoFeasibleSolution)


        # Same for the ceiling
        # Branch 2: Ceiling
        
        pivoting_ceiling.iloc[:,0] -= pivoting_ceiling.iloc[:,bnb_var_index+1] * (pivoting_ceiling.iloc[0,bnb_var_index+1] * ceil_bnb)
        pivoting_ceiling.drop([variable_names[bnb_var_index]], axis = 1)
        pivoting = copy.deepcopy(pivoting_ceiling)
        
        var_count = len(variable_names)-1
        con_count = len(constraint_names)
        
        pivoting_col_list = list(pivoting)
        times_counter = 0
        pivot_column_record = []
        pivot_row_record = []
        NoFeasibleSolution = False

        while any(pivoting.iloc[0,1:var_count+con_count+1].values<0) == True:
            times_counter += 1
        
            if times_counter <= var_count+con_count:
                pivot_column = pivoting.iloc[0,1:var_count+con_count+1].values.tolist().index(min(pivoting.iloc[0,1:var_count+con_count+1])) + 1

            else:
                pivot_list_cyc = pivoting.iloc[0,1:var_count+con_count+1].values.tolist()
                list_cyc_counter = 0
                for list_cyc_counter in range(len(pivot_list_cyc)):
                    if pivot_list_cyc[list_cyc_counter] < 0:
                        first_negative_index = list_cyc_counter
                        break
                    else:
                        list_cyc_counter += 1

                pivot_column = first_negative_index + 1
            
                # reset time counter to 0

                times_counter = 0

            pivot_column_record.append(pivot_column)
            
            test_ratios = []
            pt_i = 1

            for pt_i in range(1,con_count+1):
                try:
                    ratio = pivoting.iloc[pt_i,0] / pivoting.iloc[pt_i,pivot_column]
                except ZeroDivisionError:
                    ratio = 0

                if pivoting.iloc[pt_i,0] <= 0 and pivoting.iloc[pt_i,pivot_column] <= 0:
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
            pivoting.iloc[pivot_row,:] = pivoting.iloc[pivot_row,:] / pivot_value
            pi_count = 0
            
            for pi_count in range(con_count+1):
                if pi_count != pivot_row:
                    pivoting.iloc[pi_count,:] = pivoting.iloc[pi_count,:] - pivoting.iloc[pi_count, pivot_column] * pivoting.iloc[pivot_row,:]
                else:
                    continue
                    
                pi_count += 1

        obj_optimal = pivoting.iloc[0,0]
        slack_optimal = pivoting.iloc[1:,0].tolist()
        slack_counter = 0

        for slack_counter in range(len(pivot_row_record)):
            slack_optimal[pivot_row_record[slack_counter]-1] = 0
            slack_counter += 1

        var_optimal = [0] * var_count

        var_counter = 0

        for var_counter in range(len(pivot_row_record)):
            if pivot_column_record[var_counter] <= len(variable_names)-1:
                var_optimal[pivot_column_record[var_counter]-1] = pivoting.iloc[pivot_row_record[var_counter],0]
            else:
                slack_optimal[pivot_column_record[var_counter]-1-var_count] = pivoting.iloc[pivot_row_record[var_counter],0]
            var_counter += 1

        # in case multiple variables are assigned to the same row value, wipe the former values to 0

        repeat_counter = 0

        for repeat_counter in range(len(pivot_row_record)):
            if pivot_row_record[repeat_counter] in pivot_row_record[repeat_counter+1:]:
                if pivot_row_record[repeat_counter] <= len(variable_names)-1:
                    var_optimal[pivot_row_record[repeat_counter]-1] = 0
                else:
                    slack_optimal[pivot_row_record[repeat_counter]-1] = 0

            repeat_counter += 1
        
        # add back fixed variable (ceiling value) to the optimal solution
        
        var_optimal += [ceil_bnb]
        var_optimal.insert(bnb_var_index, var_optimal.pop())

        Ceiling_optimal_solution_Simplex = copy.deepcopy([obj_optimal, var_optimal, slack_optimal])
        Ceiling_NoFS = copy.deepcopy(NoFeasibleSolution)

        
        # Comparing Floor branch and Ceiling Branch
        
        if Floor_NoFS == True and Ceiling_NoFS == True:
            print('Error! There is NO Feasible Solutions! Maybe caused by the Triangle Situation !\n')
            break
        
        elif Floor_NoFS == True and Ceiling_NoFS == False:
            
            non_int_con_sol_obj = Ceiling_optimal_solution_Simplex[0]
            non_int_con_sol_var = Ceiling_optimal_solution_Simplex[1]
            non_int_con_sol_slack = Ceiling_optimal_solution_Simplex[2]
        
        elif Floor_NoFS == False and Ceiling_NoFS == True:
            
            non_int_con_sol_obj = Floor_optimal_solution_Simplex[0]
            non_int_con_sol_var = Floor_optimal_solution_Simplex[1]
            non_int_con_sol_slack = Floor_optimal_solution_Simplex[2]
        
        else:
            
            if int(Ceiling_optimal_solution_Simplex[0]) >= int(Floor_optimal_solution_Simplex[0]):
                
                non_int_con_sol_obj = Ceiling_optimal_solution_Simplex[0]
                non_int_con_sol_var = Ceiling_optimal_solution_Simplex[1]
                non_int_con_sol_slack = Ceiling_optimal_solution_Simplex[2]
            
            else:
                
                non_int_con_sol_obj = Floor_optimal_solution_Simplex[0]
                non_int_con_sol_var = Floor_optimal_solution_Simplex[1]
                non_int_con_sol_slack = Floor_optimal_solution_Simplex[2]
        
        # For possible further iterations, set optimal_solution_Simplex to current solution
        
        optimal_solution_Simplex = copy.deepcopy([non_int_con_sol_obj, non_int_con_sol_var, non_int_con_sol_slack])

        # check if all integer constraints are met now
        # if not, return all_int == False and iterate again
        
        int_con_sol_var = []
    
        for integer_index in Integer_Index:
            int_con_sol_var.append(optimal_solution_Simplex[1][integer_index])
            
        list_int_checker(int_con_sol_var)
        
        runtime_counter += 1
        
        if runtime_counter > int(len(variable_names) ** len(variable_names)):
            print('Error! Too Many Iterations! Maybe caused by the Triangle Situation !\n')
            NoFeasibleSolution == True
            break
        else:
            continue


    # sort the solution into the same form as Simplex Function for futher iterations
    if all_int == True:           
        obj_BB = copy.deepcopy(non_int_con_sol_obj)
        var_BB = copy.deepcopy(non_int_con_sol_var)
        slack_BB = copy.deepcopy(non_int_con_sol_slack)
        optimal_solution_Branch_and_Bound = copy.deepcopy([obj_BB, var_BB, slack_BB]) 
        NoFeasibleSolution == False
        print('\nAll integer constraints are met !\n')  
        
    else:
        NoFeasibleSolution == True
        print('\nFeasible solution is not found !\n')



# Solve Function:

def Solve():
    
    # check if integer constraints exist
    # run Simplex Algorithm if not, run Branch and Bound Algorithm otherwise
    
    try:
        Integer_Variable_Name
        
    except NameError:
        Simplex()
        
        try:
            optimal_solution_Simplex
        except NameError:
            NoFeasibleSolution = True
            print('\nNo feasible solution is found for ' + str(obj_names[0]) + ' !\n')
        else:
            NoFeasibleSolution = False
            
            output_counter = 0
            
            print('\nThe optimal solution is found for ' + str(obj_names[0]) + ' !\n')
            print('The optimal value for the objective ' + str(obj_names[0]) + ' is ' + str(optimal_solution_Simplex[0]) + ' ;\n\nWhen: \n')
          
            for output_counter in range(len(variable_names)):
                print(str(variable_names[output_counter]) + ' is set to ' + str(optimal_solution_Simplex[1][output_counter]) + '\n')
                output_counter += 1
        
    else:
        Simplex()
        Branch_And_Bound(optimal_solution_Simplex)

        try:
            optimal_solution_Branch_and_Bound
        except NameError:
            NoFeasibleSolution = True
            print('\nNo feasible solution is found for ' + str(obj_names[0]) + ' !\n')
        else:
            NoFeasibleSolution = False
            output_counter = 0
            
            print('\nThe optimal solution is found for ' + str(obj_names[0]) + ' !\n')
            print('The optimal value for the objective ' + str(obj_names[0]) + ' is ' + str(optimal_solution_Branch_and_Bound[0]) + ' ;\n\nWhen: \n')
            
            for output_counter in range(len(variable_names)):
                print(str(variable_names[output_counter]) + ' is set to ' + str(optimal_solution_Branch_and_Bound[1][output_counter]) + '\n')
                output_counter += 1


Solve()

global Deep_Copy_tableau, Deep_Copy_Simplex, Deep_Copy_NoFeasibleSolution, Deep_Copy_Branch_and_Bound

try:
    Deep_Copy_tableau = copy.deepcopy(tableau)
except NameError:
    pass

try:
    Deep_Copy_Simplex = copy.deepcopy(optimal_solution_Simplex)
except NameError:
    pass

try:
    Deep_Copy_NoFeasibleSolution = copy.deepcopy(NoFeasibleSolution)
except NameError:
    pass

try:
    Deep_Copy_Branch_and_Bound = copy.deepcopy(optimal_solution_Branch_and_Bound)
except NameError:
    pass



# The End of Solve Module
