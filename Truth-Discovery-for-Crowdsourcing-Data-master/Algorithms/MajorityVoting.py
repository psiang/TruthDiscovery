
import numpy as np
from random import randint



def majority_voting(graph):
    values_mv = {}
    for it in graph.items:
        g_count = {}
        for u in it.users:
            if u.grade[it] in g_count:
                g_count[u.grade[it]] += 1
            else:
                g_count[u.grade[it]] = 1
        max = 0
        mgrade = 0
        for key in g_count:
            if g_count[key] > max:
                max = g_count[key]
                mgrade = key
            # elif g_count[key] == max:
            #    mgrade.append(key)
        # if len(mgrade) == 1:
        #   values_mv[it] = mgrade[0]
        values_mv[it] = mgrade
    return values_mv