import sys
import os

import numpy as np

"""
Problem generation scheme proposed in:
* S. Ahn, C. Cooper, G. Cornuejols & A.M. Frieze (1988) Probabilistic analysis of a relaxation for the p-median problem.
Used in:
[1]  * P. Hansen, J. Brimberg, D. Urosevic & N. Mladenovic (2007) Primal-dual variable neighborhood search for the simple plant-location problem.
[15] * letchford2014aggressive
"""

def generate_random(n,m,min_cost,max_cost):
    facs = np.random.random((n,2))
    clis = np.random.random((m,2))
    fac_costs = min_cost+np.random.random(n)*(max_cost-min_cost)
    # print("facs:")
    # print(facs)
    # print("clis:")
    # print(clis)
    #
    dst_x = np.expand_dims(facs[:,0],1)-np.expand_dims(clis[:,0],0)
    dst_y = np.expand_dims(facs[:,1],1)-np.expand_dims(clis[:,1],0)
    dists = (dst_x**2+dst_y**2)**0.5
    # -- rounding
    dists = np.floor(dists*5000).astype('int')
    fac_costs = np.floor(fac_costs*5000).astype('int')
    #
    return fac_costs,dists

def save_problem_simple(fname,fcosts,dists,p_limit=0):
    assert(fcosts.size==dists.shape[0])
    fi = open(fname,'w')
    fi.write("FILE: %s\n"%os.path.basename(fname))
    fi.write("%d %d %d\n"%(dists.shape[0],dists.shape[1],p_limit))
    for i in range(dists.shape[0]):
        fi.write("%d %d "%(i+1,fcosts[i]))
        for j in range(dists.shape[1]):
            fi.write("%d"%dists[i,j])
            if j!=dists.shape[1]-1:
                fi.write(" ")
            else:
                fi.write("\n")
    fi.close()

def save_problem_lpsolve(fname,fcosts,dists,p_limit=0):
    assert(fcosts.size==dists.shape[0])
    n = fcosts.size
    m = dists.shape[1]
    #
    fi = open(fname,'w')
    # -- objective function
    fi.write("min: ")
    for i in range(n):
        if fcosts[i]>0: fi.write(" +%s X%d"%(fcosts[i],i))
    for j in range(m):
        for i in range(n):
            fi.write(" +%d Y%dc%d"%(dists[i][j],j,i))
    fi.write(";\n\n")
    # -- limit opened facilities
    if p_limit>0:
        for i in range(n):
            fi.write(" +X%d"%i)
        fi.write(" <= %d"%p_limit)
        fi.write(";\n\n")
    # -- only one facility restriction
    for j in range(m):
        for i in range(n):
            fi.write("+Y%dc%d "%(j,i))
        fi.write(">= 1;\n") # NOTE: Is better than '='?
    fi.write("\n")
    # --
    for i in range(n):
        for j in range(m):
            fi.write("Y%dc%d <= X%d;\n"%(j,i,i))
    fi.write("\n")
    # --
    fi.write("bin "+",".join(["X%d"%i for i in range(n)])+";\n\n")
    # --
    fi.close()

MODES = {
    's': lambda n: (n**0.5/1000.0,n**0.5/1000.0),
    'm': lambda n: (n**0.5/100.0, n**0.5/100.0 ),
    'l': lambda n: (n**0.5/10.0,  n**0.5/10.0  ),
    'v': lambda n: (n**0.5/1000.0,n**0.5/10.0  ),
    }

if __name__ == '__main__':
    if len(sys.argv)!=5:
        print("usage: %s <n> (s|m|l|v|<cost>|p_<p>) <fname> <lpfname>"%(sys.argv[0]))
        sys.exit(1)
    n = int(sys.argv[1])
    if len(sys.argv[2])>2 and 'p_'==sys.argv[2][:2]:
        min_c,max_c = (0,0)
        p_limit = int(sys.argv[2][2:])
    elif sys.argv[2] in MODES:
        min_c,max_c = MODES[sys.argv[2]](n)
        p_limit = 0
    else:
        min_c,max_c = (float(sys.argv[2]),float(sys.argv[2]))
        p_limit = 0
    #
    fname = sys.argv[3]
    lpfname = sys.argv[4]
    fcosts,dists = generate_random(n,n,min_c,max_c)
    save_problem_simple(fname,fcosts,dists,p_limit)
    save_problem_lpsolve(lpfname,fcosts,dists,p_limit)
