import os

def get_dirs(dir,ext=None,deep=None):
    dirs = []
    if deep is None or deep>0:
        for subdir in os.listdir(dir):
            subdir_path = os.path.join(dir,subdir)
            if os.path.isdir(subdir_path):
                contents = get_dirs(subdir_path,ext,None if deep is None else deep-1)
                dirs += [[subdir]+x for x in contents]
            else:
                if ext is None or (len(subdir)>=len(ext) and subdir[-len(ext):]==ext):
                    dirs += [[subdir]]
    else:
        dirs = [[]]
    return dirs

def read_opt_val(fname,rounding):
    fi = open(fname)
    for lin in fi:
        lin = lin.strip()
        res = float(lin.split(' ')[-1])
        if rounding:
            res = int(round(res))
        break
    fi.close()
    return res

def extract_field(fname,field,func=float):
    fil = open(fname)
    value = None
    for lin in fil:
        if ":" in lin:
            lin = lin.strip()
            fie,val = lin.split(":")
            while fie[0]==" ":
                fie = fie[1:]
            if fie==field:
                value = func(val)
                break
    fil.close()
    return value
