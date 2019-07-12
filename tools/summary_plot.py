import os
import numpy as np
import matplotlib.pyplot as plt

from file_navigation import *

# Fields to plot:
FIELDS = [
    {
        "attr_name":"Value",
        "file_name":"value",
        "plot_name":"Mean error",
        "value": lambda vals,opts: np.mean((-vals/opts)-1),
    },
    {
        "attr_name":"# Time",
        "file_name":"time",
        "plot_name":"Mean time",
        "value": lambda vals,opts: np.mean(vals),
    },
]

PROBLEM_DIR = "custom"
OPT_EXTENSION = ".opt"
RESULTS_DIR = "res"
ROUNDING = True


if __name__ == '__main__':
    # Get the directories:
    opt_dirs = get_dirs(PROBLEM_DIR,OPT_EXTENSION)
    # Get the kinds, p's, and n's available
    transf = lambda dirs,i: sorted(list(set(x[0].split("_")[i] for x in dirs)))
    kinds = transf(opt_dirs,0)
    ps = sorted([int(x) for x in transf(opt_dirs,1)])
    ns = sorted([int(x) for x in transf(opt_dirs,2)])
    # Algorithm variants:
    variants = sorted(list(set(x[0] for x in get_dirs(RESULTS_DIR,deep=2) if x[1]==PROBLEM_DIR)))


    # Get optima by problem group:
    optima = {}
    for kind in kinds:
        for p in ps:
            for n in ns:
                group_name = "%s_%s_%s"%(kind,p,n)
                prob_dir = os.path.join(PROBLEM_DIR,group_name)
                problems = get_dirs(prob_dir,ext='.opt')
                # For each problem
                optima[(kind,p,n)] = {}
                for prob in problems:
                    full_problem_path = os.path.join(prob_dir,prob[0])
                    optima[(kind,p,n)][prob[0]] = read_opt_val(full_problem_path,ROUNDING)

    # Problem kind (splp, p-median)
    for kind in kinds:
        # Field name: -> new plot
        for field in FIELDS:
            fig, axs = plt.subplots(nrows=1,ncols=len(ps),sharex=True,sharey=True,figsize=(14,5))
            lines = {}
            colors = {}
            # Value of p -> new sub-plot
            for i,p in enumerate(ps):
                ax = axs[i]
                ax.grid()
                ax.set_title("$p{=}%s$"%p)
                # Variant -> new line
                for vari in variants:
                    valid_variant = True
                    points_y = []
                    # Value of n -> new point
                    for n in ns:
                        # Get the optimal values
                        opti_vals = optima[(kind,p,n)]
                        prob_names = sorted(opti_vals.keys())
                        # Get variant results
                        group_name = "%s_%s_%s"%(kind,p,n)
                        prob_dir = os.path.join(PROBLEM_DIR,group_name)
                        res_dir = os.path.join(RESULTS_DIR,vari,prob_dir)
                        #
                        value_and_opt = []
                        for prob in prob_names:
                            opt = opti_vals[prob]
                            res_fname = os.path.join(res_dir,prob.replace('.opt','_ls'))
                            if not os.path.isfile(res_fname):
                                valid_variant = False
                                break
                            field_v = extract_field(res_fname,field["attr_name"],func=float)
                            value_and_opt.append( (field_v,opt) )
                        if not valid_variant:
                            break
                        value_and_opt = np.array(value_and_opt)
                        vals = value_and_opt[:,0]
                        opts = value_and_opt[:,1]
                        value = field["value"](vals,opts)
                        print("%s %s %s"%(prob_dir,vari,value))
                        points_y.append(value)
                    if valid_variant:
                        # Plot on this axis
                        if vari not in colors:
                            colors[vari] = 'C'+str(len(colors))
                        lines[vari] = ax.plot(ns,points_y,label=vari,c=colors[vari])[0]
                #
            #
            fig.suptitle("%s for %s"%(field["plot_name"],kind))
            fig.legend(lines.values(),lines.keys(),
                loc='upper center',bbox_to_anchor=(0.5, 0.85),ncol=4,fancybox=True)
            fig.savefig(kind+"_"+field["file_name"].lower()+".png")
        #
