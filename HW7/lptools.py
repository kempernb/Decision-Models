# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 19:48:23 2021

@author: soxcr
"""
## This code will display an algebraic representation
## of an OR Tools Glop optimization model labeled mymodel.
## ver. 0.1, 10/22/2020, C. Sox
## ver. 0.2, 11/07/2020, C.Sox : fix display of negative coefficients using abs()

def print_model(mymodel):
    infinity = mymodel.infinity()
    
    # Variables
    var_lst = mymodel.variables()
    var_str = ''
    first_var = True
    for var in var_lst:
        if first_var:
            var_str = var_str + str(var)
            first_var = False
        else:
            var_str = var_str + ', ' + str(var) 
    print('Variables:')
    print(var_str, '\n')
    
    # Objective
    if mymodel.Objective().maximization():
        obj_str = 'maximize: '
    elif mymodel.Objective().minimization():
        obj_str = 'minimize: '
    else:
        obj_str = 'undefined: '
        
    first_var = True
    for var in var_lst:
        coeff = mymodel.Objective().GetCoefficient(var)
        if coeff < 0:
            obj_str = obj_str + '- ' + str(abs(coeff)) + '*' + str(var) + ' '
            if first_var: first_var = False
        if first_var and coeff > 0:
            obj_str = obj_str + str(coeff) + '*' + str(var) + ' '
            first_var = False
        elif coeff > 0:
            obj_str = obj_str + '+ ' + str(coeff) + '*' + str(var) + ' '
    print(obj_str + '\n')
    
    # Constraints
    print('Subject To:')
    constr_lst = mymodel.constraints()
    for c in constr_lst:
        constr_str = c.name() + ': '
        first_var = True
        for var in var_lst:
            coeff = c.GetCoefficient(var)
            if coeff < 0:
                constr_str = constr_str + '- ' + str(abs(coeff)) + '*' + str(var) + ' '
                if first_var: first_var = False
            elif first_var and coeff > 0:
                constr_str = constr_str + str(coeff) + '*' + str(var) + ' '
                first_var = False
            elif coeff > 0:
                constr_str = constr_str + '+ ' + str(coeff) + '*' + str(var) + ' '
        lower = c.lb()
        upper = c.ub()
        if lower == upper:
            print(constr_str + '= ' + str(lower))
        elif lower > -infinity and upper == infinity:
            print(constr_str + '>= ' + str(lower))
        elif lower == -infinity and upper < infinity:
            print(constr_str + '<= ' + str(upper))
        elif lower > -infinity and upper < infinity:
            print(constr_str + '>= ' + str(lower))
            print(constr_str + '<= ' + str(upper))
    print('')
            
    # Variable Bounds
    print('Bounds:')
    for var in var_lst:
        lower = var.lb()
        upper = var.ub()
        if lower > -infinity and upper == infinity:
            print(str(var) + ' >= ' + str(lower))
        elif lower == -infinity and upper < infinity:
                print(str(var) + ' <= ' + str(upper))
        elif lower > -infinity and upper < infinity:
            print(str(lower) + ' <= ' + str(var) + ' <= ' + str(upper))    
