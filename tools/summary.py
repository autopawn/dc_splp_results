import os
import sys
import numpy as np

from file_navigation import *

DEEPNESS=1

# -- --

def read_optimum(fname):
    fi = open(fname)
    nfacs_rep = None
    time = None
    k = None
    for lin in fi:
        lin = lin.strip()
        lin = lin.replace("  "," ")
        if len(lin)==0: continue
        if "#" in lin:
            if "#runtime:" in lin:
                time = int(lin.replace("#runtime:",""))
            if "#nfacs:" in lin:
                nfacs_rep = int(lin.replace("#nfacs:",""))
        else:
            k = lin.split()
    fi.close()
    assert(k)
    assigns = [int(x) for x in k[:-1]]
    if not (nfacs_rep is None or len(set(assigns))<=nfacs_rep):
        print(fname)
        print(nfacs_rep)
        assert(False)
    value = float(k[-1])
    return assigns,value,time

def read_problem(fname):
    fi = open(fname)
    mode = 0
    for lin in fi:
        lin=lin.strip()
        if "FILE" in lin:
            mode = 1
            continue
        if mode==0:
            n,m = [int(x) for x in lin.split(' ')]
            p = 0
        else:
            n,m,p = [int(x) for x in lin.split(' ')]
        break
    fi.close()
    return n,m,p

def read_solution(fname):
    if not os.path.isfile(fname):
        return None,None,None,None,None
    # ---
    fi = open(fname)
    assigns = None
    value = None
    time = None
    iters = None
    finalsols = None
    for lin in fi:
        if "# Time:" in lin:
            time = float(lin.split(" ")[-1])
        if "# Iterations:" in lin:
            iters = float(lin.split(" ")[-1])
        if "# Final_solutions:" in lin:
            finalsols = float(lin.split(" ")[-1])
        if (assigns is None) and ("Assigns:" in lin):
            assigns = [int(x) for x in lin.split()[1:]]
        if (value is None) and ("Value:" in lin):
            value = -float(lin.split()[1])
        if (assigns is not None) and (value is not None):
            break
    fi.close()
    assert(assigns is not None)
    assert(value is not None)
    assert(time is not None)
    #
    return assigns,value,time,iters,finalsols

def is_optimum(sol,opt,can_be_better):
    opt_assi = opt[0]
    opt_val = opt[1]
    sol_assi = sol[0]
    sol_val = sol[1]
    if sol_assi is None:
        assert(sol_val is None)
        return 0
    sol_facts = set(sol_assi)
    opt_facts = set(opt_assi)
    if sol_facts == opt_facts: return 1
    if sol_val <= opt_val:
        if sol_val<=opt_val-0.01:
            assert(can_be_better)
            return 2
        else:
            return 1
    return 0

if __name__ == '__main__':

    # -- parse input --
    if len(sys.argv)!=3:
        print("usage: python %s <prob_dir> <sols_dir>"%(sys.argv[0]))
        print("e.g.:  python %s %s %s"%(sys.argv[0],'splp','res/dc_norm_s_200_400/splp'))
        sys.exit(1)

    prob_dir = sys.argv[1]
    sols_dir = sys.argv[2]


    problems = {}
    problems['opt'] = get_dirs(prob_dir,".opt")
    problems['bub'] = get_dirs(prob_dir,".bub")

    # Grand totals
    total_perces = []
    total_times = []
    total_times_ls = []
    total_iters = []
    total_finals = []
    total_optis = 0

    summary = {}
    for kind in ('opt','bub'):
        summary[kind] = []
        print("="*80)
        print("> PROBLEMS: "+kind.upper())
        print("="*80)
        prob_names = sorted(list(problems[kind]))
        # Identify the problem groups (last folders):

        get_group = lambda x: tuple(x[:-1] if len(x)<=DEEPNESS else x[:DEEPNESS])
        group_names = sorted(list(set([get_group(x) for x in prob_names])))

        # --- Table
        table = []
        # ---

        if kind=='bub':
            # Metrics only for .bub
            bub_perces = []
            bub_times = []
            bub_times_ls = []
            bub_iters = []
            bub_finals = []
            bub_optis = 0
            bub_betters = 0

        for group in group_names:
            group_name = '/'.join(group)
            if group_name=='kmedian': continue #NOTE: hardcoded exlcusion of kmedian

            # Find the specific problems for this group:
            group_prob_names = [x for x in prob_names if get_group(x)==group]

            strbases = {}
            nfacs = []
            nclis = []
            opt_nfacs = []
            ps = []
            opt_times = []


            for prob in group_prob_names:
                joined = os.path.join(*prob)
                opt_fname = os.path.join(prob_dir,joined)
                prob_fname = opt_fname.replace('.'+kind,'')
                if not os.path.isfile(prob_fname):
                    print("ERROR: %s does not exists."%prob_fname)
                    sys.exit(1)
                n,m,p = read_problem(prob_fname)
                nfacs.append(n)
                nclis.append(m)
                ps.append(p)
                opt_data = read_optimum(opt_fname)
                # --- Maximums
                n_opt_facilities = len(set(opt_data[0]))
                n_clients = len(opt_data[0])
                opt_nfacs.append(n_opt_facilities)
                if opt_data[2] is not None:
                    opt_times.append(opt_data[2])
                strbases[prob_fname] = "%-35s  n:%5d  on:%5d  ov:%9.3f"%(
                    joined,n_clients,n_opt_facilities,opt_data[1])

            # Print problem and opt solutions description
            print("-"*20)
            min_p = np.min(ps)
            max_p = np.max(ps)
            str_p = str(min_p) if min_p==max_p else "%d-%d"%(min_p,max_p)
            min_nfacs = np.min(nfacs)
            max_nfacs = np.max(nfacs)
            str_nfacs = str(min_nfacs) if min_nfacs==max_nfacs else "%d-%d"%(min_nfacs,max_nfacs)
            min_nclis = np.min(nclis)
            max_nclis = np.max(nclis)
            str_nclis = str(min_nclis) if min_nclis==max_nclis else "%d-%d"%(min_nclis,max_nclis)
            min_opt_nfacs = np.min(opt_nfacs)
            max_opt_nfacs = np.max(opt_nfacs)
            str_opt_nfacs = str(min_opt_nfacs) if min_opt_nfacs==max_opt_nfacs else "%d-%d"%(min_opt_nfacs,max_opt_nfacs)
            opt_time_mean = float('inf') if len(opt_times)==0 else np.mean(opt_times)
            opt_time_std = float('inf') if len(opt_times)==0 else np.std(opt_times)

            print("%-35s  (%d probs)  n:%s  m:%s  p:%s  on:%s  otime: %.2f+-%.2f"%(group_name,
                len(group_prob_names),
                str_nfacs,
                str_nclis,
                str_p,
                str_opt_nfacs,
                opt_time_mean,opt_time_std))

            for mode in ('','_ls'):
                strings = []
                perces = []
                perces_all = []
                times = []
                iters = []
                finals = []
                optis = 0
                betters = 0
                nones = 0
                for prob in group_prob_names:
                    joined = os.path.join(*prob)
                    # --- Get the solution
                    sol_fname = os.path.join(sols_dir,joined)
                    sol_fname = sol_fname[:-4]
                    sol_data = read_solution(sol_fname+mode)
                    opt_fname = os.path.join(prob_dir,joined)
                    opt_data = read_optimum(opt_fname)
                    prob_fname = opt_fname.replace('.'+kind,'')
                    # --- Check for optimality
                    perce = 0
                    show = False
                    if sol_data[0] is None:
                        nones += 1
                    else:
                        opt = is_optimum(sol_data,opt_data,kind=='bub')
                        if opt==1:
                            optis += 1
                        elif opt==2:
                            betters += 1
                        else:
                            show = True
                        perce = 0 if opt_data[1] is None else sol_data[1]/opt_data[1]
                        times.append(sol_data[2])
                        iters.append(sol_data[3])
                        finals.append(sol_data[4])
                    if show:
                        if mode=='_ls':
                            strings.append(strbases[prob_fname]+"  v:%9.3f %8.4f"%(
                                sol_data[1],perce))
                    if (show or kind=='bub') and perce!=0:
                        perces.append(perce)
                    if perce!=0:
                        perces_all.append(perce)
                    else:
                        print("\033[0;31m WARNING: perces=0!!!! \033[0m")
                # For the all summary:
                if kind=='bub':
                    if mode=='_ls':
                        bub_perces += perces_all
                        bub_times_ls += times
                        bub_iters += iters
                        bub_finals += finals
                        bub_optis += optis
                        bub_betters += betters
                    else:
                        bub_times += times

                if mode=='_ls':
                    total_perces += perces_all
                    total_times_ls += times
                    total_iters += iters
                    total_finals += finals
                    total_optis += optis+betters
                else:
                    total_times += times
                # Print solutions description
                if nones==0:
                    red = ''
                    noc = ''
                else:
                    red = '\033[0;31m'
                    noc = '\033[0m'
                perce = "    -    " if len(perces)==0 else "%9.6f"%(np.mean(perces))
                time = "    -    " if len(times)==0 else "%8.3f+-%-8.3f"%(np.mean(times),np.std(times))
                time2 = "    -    " if len(times)==0 else "%8.3f-%-8.3f"%(np.min(times),np.max(times))
                iter = "   -   "if len(iters)==0 else "%3d-%-3d"%(np.min(iters),np.max(iters))
                final = "   -   "if len(finals)==0 else "%3d-%-3d"%(np.min(finals),np.max(finals))
                print("%-35s  opt:%3d/%-3d  %snons:%3d/%-3d%s  perce:%s  t:%s  it:%s  fs:%s"%(
                    sols_dir+('' if mode=='' else "("+mode+")"),
                    optis,len(group_prob_names),
                    red,nones,len(group_prob_names),noc,
                    perce,time,iter,final))
                for stri in strings:
                    print(stri)
                # --- Table
                n_probs = len(group_prob_names)
                if nones<n_probs:
                    if mode=='':
                        preoptis = optis
                    else:
                        fst = "\\hline" if len(table)==0 else ""
                        if kind=='opt':
                            table.append("\\\\ %s %s & $%d/%d$ & $%d/%d$ & %s & %s & %s "%(fst,group_name,optis,n_probs,preoptis,n_probs,perce,time2,iter))
                        else:
                            table.append("\\\\ %s %s & $%d/%d$ & $%d/%d$ & %s & %s & %s "%(fst,group_name,betters,n_probs,optis,n_probs,perce,time2,iter))
                # ---
        table = "\n".join(table)
        
        if kind=='opt':
            print("="*20+" BEGINTABLE_KNOWN")
        else:
            print("="*20+" BEGINTABLE_UNKNOWN")
        
        if kind=='opt':
            print("\\hline \\textbf{Benchmark} & \\textbf{Optima} & \\textbf{Opt. pre-LS} & \\textbf{Non opt. cost} & \\textbf{CPU time} [s] & \\textbf{Iters.}")
        else:
            print("\\hline \\textbf{Benchmark} & \\textbf{Better} & \\textbf{Same} & \\textbf{Mean rel. cost} & \\textbf{CPU time} [s] & \\textbf{Iters.}")

        print(table)
        # print("\\\\ \\hline")
        
        if kind=='opt':
            print("="*20+" ENDTABLE_KNOWN")
        else:
            print("="*20+" ENDTABLE_UNKNOWN")

    # Grand totals table row:
    n_probs = len(total_perces)
    total_perces = np.mean(total_perces)
    total_times = np.sum(total_times)
    total_times_ls = np.sum(total_times_ls)
    total_time_ls_per = 100*(total_times_ls-total_times)/total_times_ls
    total_iters = np.mean(total_iters)
    total_finals = np.mean(total_finals)
    print("% TOTALS:")
    print("\\hline \\textbf{Strategy} & \\textbf{Optima} & $\\bar{X}$ \\textbf{rel. cost} & \\textbf{Time}[s] & \\textbf{Time LS}[\%] & $\\bar{X}$ \\textbf{iters.} & $\\bar{X}$ \\textbf{local opt.}")
    nam = sys.argv[2].replace("_","\_")
    print("\\\\ %s & $%d/%d$ & $%f$ & $%.0f$ & $%.2f$ & $%.3f$ & $%.3f$"%(nam,total_optis,n_probs,total_perces,total_times_ls,total_time_ls_per,total_iters,total_finals))

    # Bub totals table row:
    bub_n_probs = len(bub_perces)
    bub_worst = bub_n_probs-bub_optis-bub_betters
    bub_perces = np.mean(bub_perces)
    bub_times = np.sum(bub_times)
    bub_times_ls = np.sum(bub_times_ls)
    bub_time_ls_per = 100*(bub_times_ls-bub_times)/bub_times_ls
    bub_iters = np.mean(bub_iters)
    bub_finals = np.mean(bub_finals)

    print("% BUB:")
    # print("\\hline \\textbf{Strategy} & \\textbf{Better} & \\textbf{Same} & \\textbf{Worse} & $\\bar{X}$ \\textbf{rel. cost} & \\textbf{Time}[s] & \\textbf{Time LS}[\%] & \\textbf{Iters.}")
    # print("\\\\ %s & $%d$ & $%d$ & $%d$ & $%.6f$ & $%.0f$ & $%.2f$ & $%.3f$ "%(nam,bub_betters,bub_optis,bub_worst,bub_perces,bub_times_ls,bub_time_ls_per,bub_iters))
    print("\\hline \\textbf{Strategy} & \\textbf{Better} & \\textbf{Same} & \\textbf{Worse} & $\\bar{X}$ \\textbf{rel. cost} & \\textbf{Time}[s] & \\textbf{Time LS}[\%]")
    print("\\\\ %s & $%d$ & $%d$ & $%d$ & $%.6f$ & $%.0f$ & $%.2f$"%(nam,bub_betters,bub_optis,bub_worst,bub_perces,bub_times_ls,bub_time_ls_per))
