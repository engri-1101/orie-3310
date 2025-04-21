from tabulate import tabulate
import numpy as np
from IPython.display import display, Markdown
from pulp import *

def simplex_tableau(lp):
    # gets the variables of the model
    lp_vars = lp.variables()
    num_basic = len(lp.constraints)
    # checks reduced costs to find basic variables
    basic_vars = sorted([k for k in lp_vars], key=lambda x: abs(x.to_dict()['dj']))[:num_basic]
    # basic_vars = [k for k in lp_vars if round(k.to_dict()['dj'],5) == 0][:num_basic]
    def get_coeff(cons, var):
        d = cons[1]
        for v, val in d.items():
            if v.to_dict()['name'] == var.to_dict()['name']:
                return val
        return 0
    # A is the matrix with the coefficients of the constraints
    A = np.array([[get_coeff(c, i) for i in lp_vars] for c in lp.constraints.items()])
    # B is A limited on columns of basic variables
    basic_varnames = set([i.to_dict()['name'] for i in basic_vars])
    B = A[:,[k for k in range(len(lp_vars)) if lp_vars[k].to_dict()['name'] in basic_varnames]]
    bar_A =  np.round(np.dot(np.linalg.inv(B),A),5)
    temp = [[basic_vars[i].to_dict()['name']]+bar_A.tolist()[i]+[round(value(basic_vars[i]),5)] 
            for i in range(len(basic_vars))]
    table = tabulate([
        ['Reduced costs $\\bar{c}_j$']
            + [round(v.to_dict()['dj'],5) for v in lp_vars]
            + ['$\\bar{b}_i$']]+temp, 
       headers=(['']+lp_vars+['']), tablefmt='github')
    display(Markdown(table))
    return (bar_A, [(i.to_dict()['name'],round(value(i),5)) for i in basic_vars],
           [int(str(k)[1:]) for k in lp_vars if round(k.to_dict()['dj'],5) != 0])
