def simplex_tableau(lp):
    from tabulate import tabulate
    import numpy as np
    from IPython.display import display, Markdown
    from ortools.linear_solver import pywraplp

    # gets the variables of the model
    lp_vars = lp.variables()
    num_basic = lp.NumConstraints()
    # checks reduced costs to find basic variables
    basic_vars = [k for k in lp_vars if round(k.ReducedCost(),5) == 0][:num_basic]
    # A is the matrix with the coefficients of the constraints
    A = np.array([[c.GetCoefficient(i) for i in lp_vars] for c in lp.constraints()])
    # B is A limited on columns of basic variables
    B = A[:,[k for k in range(len(lp_vars)) if lp_vars[k].name() 
        in [i.name() for i in basic_vars]]]
    bar_A =  np.round_(np.dot(np.linalg.inv(B),A),5)
    temp = [[basic_vars[i].name()]+bar_A.tolist()[i]+[round(basic_vars[i].solution_value(),5)] 
            for i in range(len(basic_vars))]
    table = tabulate([
        ['Reduced costs $\\bar{c}_j$']
            + [round(v.ReducedCost(),5) for v in lp_vars]
            + ['$\\bar{b}_i$']]+temp, 
       headers=(['']+lp_vars+['']), tablefmt='github')
    display(Markdown(table))
    return (bar_A, [(i.name(),round(i.solution_value(),5)) for i in basic_vars],
           [int(str(k)[1:]) for k in lp_vars if round(k.ReducedCost(),5) != 0])

def reset(lp):
    from ortools.linear_solver import pywraplp
    # gets the variables of the model
    lp_vars = lp.variables()
    # get var coefficients in obj function
    obj_coeff = {i:lp.Objective().GetCoefficient(i) for i in lp_vars}
    lp.Objective().Clear()
    # add the same obj func
    lp.Objective().SetMaximization()
    for i in lp_vars:
        lp.Objective().SetCoefficient(i, obj_coeff[i])
