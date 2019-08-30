__author__ = 'JasonLee'

import sys
import subprocess
import os

sep = ","
exec_cs = True

def gete2wlandw2el(answer_filename):
    answer_list = []

    with open(answer_filename) as f:
        f.readline()
        for line in f:
            if not line:
                continue
            parts = line.strip().split(sep)
            worker_name, item_name, worker_label = parts[:3]
            answer_list.append([worker_name, item_name, worker_label])

    os.chdir(os.path.dirname(__file__))

    with open("Data/CF.csv", "w") as f:
        for piece in answer_list:
            f.write(",".join(piece) + "\n")

def Run():
    if exec_cs:
        subprocess.getstatusoutput("rm Results/endpoints.csv")
        subprocess.getstatusoutput("CommunityBCCSourceCode.exe")

    e2lpd = {}
    with open("Results/endpoints.csv") as f:
        for line in f:
            parts = line.strip().split(sep)
            e2lpd[parts[0]] = {}
            for i, v in enumerate(parts[1:]):
                e2lpd[parts[0]][str(i)] = float(v)

    return e2lpd

