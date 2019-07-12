import sys

from file_navigation import *

PROBLEMS_DIR = ["custom","pmedian","pmedianlarge","splp","splpkmedian"]
RESULTS_DIR = "res"

assert(len(sys.argv)==2)

prob_dirs = []
for prob_main_dir in PROBLEMS_DIR:
    dirs = get_dirs(prob_main_dir,deep=1)
    prob_dirs += [[prob_main_dir]+x for x in dirs]
prob_dirs = sorted(prob_dirs)
joined_prob_dirs = [os.path.join(*x) for x in prob_dirs]

# Algorithm variants:
variants = list(set(x[0] for x in get_dirs(RESULTS_DIR,deep=2)))
variants = sorted([(v.split('_')[0],v.split('_')[1],int(v.split('_')[2]),int(v.split('_')[3]),v) for v in variants])
variants = [x[-1] for x in variants]


len_name = max([len(x) for x in joined_prob_dirs])
texts = [[" "*len_name]]
for variant in variants:
    texts[0].append(variant)
for p,prob_dir in enumerate(prob_dirs):
    probs = [prob_dir+x for x in get_dirs(os.path.join(*prob_dir),ext='.opt')]
    texts.append([joined_prob_dirs[p]+" "*(len_name-len(joined_prob_dirs[p]))])
    for variant in variants:
        count = 0
        for prob in probs:
            full_path = [RESULTS_DIR,variant]+prob
            full_path = os.path.join(*full_path).replace(".opt","_ls")
            if os.path.isfile(full_path):
                count += 1
        if count==len(probs):
            texts[-1].append("#"*len(variant))
        elif count==0:
            texts[-1].append("."*len(variant))
        else:
            texts[-1].append("?"*len(variant))

fil = open(sys.argv[1],'w')
for line in texts:
    fil.write("|".join(line)+"\n")
fil.close()
