import numpy as np
from numpy import genfromtxt
from collections import namedtuple
import random
import math
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score

import item_model
import user_model
import graph_builder
from CrowdsourcingAlg.Algorithms import MajorityVoting
from CrowdsourcingAlg.Algorithms import WeightedVoting
from CrowdsourcingAlg.Algorithms import ExpectationMaximization
from CrowdsourcingAlg.Algorithms import DavidSkene_EM



# Calculate the accuracy of the results
def getAcc(values, its):
    estimation = []
    q = []
    for it in its:
        estimation.append(values[it])
        q.append(it.q)
    acc = accuracy_score(q, estimation)
    return acc

# Get the F measure for the results
def getFM(values, its):
    estimation = []
    q = []
    for it in its:
        estimation.append(values[it])
        q.append(it.q)
    f1_weighted = f1_score(q, estimation, average='weighted')
    return f1_weighted

filename_l = '../../Data/AdultContent2/labels.csv'
labels = genfromtxt(filename_l, delimiter=',', dtype=None)

filename_gold = '../../Data/AdultContent2/gold.csv'
gold = genfromtxt(filename_gold, delimiter=',', dtype=None)

# labels file: col[0]-worker id, col[1]-url, col[2]-label. Label 'B' probably means broken link
# gold file: col[0]-url, col[1]-gold truth, there is no gold as 'B'

def MapLabel(lc):
    if lc == 'G':
        return 1
    elif lc == 'P':
        return 2
    elif lc == 'R':
        return 3
    elif lc == 'X':
        return 4
    elif lc == 'B':
        return 5

# Map labels {G, P, R, X, B} to {1, 2, 3, 4, 5}
data = []
for l in labels:
    n = MapLabel(l[2])
    data.append([l[0], l[1], n])
gold_hm = {}
for g in gold:
    n = MapLabel(g[1])
    gold_hm[g[0]] = n
print "Num of items: ", len(gold_hm)
G_SCALE = [1, 2, 3, 4, 5]

item_data = {}
worker_data = {}
for di in data:
    if di[0] not in worker_data:
        worker_data[di[0]] = 1
    if di[1] not in item_data:
        item_data[di[1]] = 1
print "Num of items in unfiltered data: ", len(item_data)
print "Num of workers in unfiltered data: ", len(worker_data)

# filter the labels, only consider items with gold
filtered_data = []
for l in data:
    if l[2] == 5:
        continue
    elif l[1] in gold_hm:
        filtered_data.append(l[:])
print "Total num of labels for selected items: ", len(filtered_data)


# deal with workers who have >1 labels for the same item
user_multi = {}
uit = namedtuple("uit", ["uid", "url"])
for fl in filtered_data:
    ui = uit(uid=fl[0], url=fl[1])
    if ui in user_multi:
        user_multi[ui].append(fl[2])
    else:
        user_multi[ui] = []
        user_multi[ui].append(fl[2])
mulNum = 0
# randomly choose one of the worker's label as his given label
user_multi_label = {}
for k in user_multi:
    if len(user_multi[k]) > 1:
        mulNum += 1
        rand = random.randint(0, len(user_multi[k])-1)
        user_multi_label[k] = user_multi[k][rand]
print "Multi labels per user/item: ", mulNum

filtered_data_repl = []
added = {}
for fl in filtered_data:
    ui = uit(uid=fl[0], url=fl[1])
    if ui in added:
        continue
    else:
        added[ui] = 1
        if ui in user_multi_label:
            filtered_data_repl.append([fl[0], fl[1], user_multi_label[ui]])
        else:
            filtered_data_repl.append(fl[:])
print "New num of filtered labels: ", len(filtered_data_repl)


# user hashmap
user_hm = {}
for flr in filtered_data_repl:
    if flr[0] in user_hm:
        user_hm[flr[0]].append([flr[1], flr[2]])
    else:
        user_hm[flr[0]] = []
        user_hm[flr[0]].append([flr[1], flr[2]])
print "Num of users: ", len(user_hm)

# item hashmap
item_hm = {}
for flr in filtered_data_repl:
    if flr[1] in item_hm:
        item_hm[flr[1]].append(flr[0])
    else:
        item_hm[flr[1]] = []
        item_hm[flr[1]].append(flr[0])
print "Num of items in filtered dataset: ", len(item_hm)
gold_truths = {}
for it in item_hm:
    if it in gold_hm:
        gold_truths[it] = gold_hm[it]
print "Len of gold_truths: ", len(gold_truths)

# build the graph
items = [item_model.Item(gold_truths[gt], gt) for gt in gold_truths]
users = [user_model.User(u) for u in user_hm]

itid = 0
for it in items:
    it.id = itid
    itid += 1
uid = 0
for u in users:
    u.name = uid
    uid += 1

graph = graph_builder.Graph(users, items)
for it in items:
    for uit in item_hm[it.url]:
        graph.pick_user(it, uit)
for u in users:
    for itl in user_hm[u.id]:
        graph.pick_item(u, itl[0], itl[1])

# check correct mapping
print "Num of graph items: ", len(items)
print "Num of graph users: ", len(users)
numl = 0
for u in graph.users:
    numl += len(u.grade)
print "Num of graph labels: ", numl
fdr_ul = {}
graph_ul = {}
for fdr in filtered_data_repl:
    if fdr[0] in fdr_ul:
        fdr_ul[fdr[0]].append(fdr[2])
    else:
        fdr_ul[fdr[0]] = []
        fdr_ul[fdr[0]].append(fdr[2])
for u in graph.users:
    graph_ul[u.id] = []
    for it in u.items:
        graph_ul[u.id].append(u.grade[it])
for k in fdr_ul:
    if fdr_ul[k] <> graph_ul[k]:
        print "Incorrect mapping for user id: ", k


# MV
values_via_MV = MajorityVoting.majority_voting(graph)

# weighted voting
values_via_WV = WeightedVoting.weighted_voting_cat(graph, G_SCALE)

# EM
user_reliability_em, values_via_EM = ExpectationMaximization.emMultiClass(graph, G_SCALE).expectation_maximization()

# DS
values_via_DS = DavidSkene_EM.ds_em(graph).DS()

# Get measurement metrics
acc_mv = getAcc(values_via_MV, items)
acc_wv = getAcc(values_via_WV, items)
acc_em = getAcc(values_via_EM, items)
acc_ds = getAcc(values_via_DS, items)

f1_mv = getFM(values_via_MV, items)
f1_wv = getFM(values_via_WV, items)
f1_em = getFM(values_via_EM, items)
f1_ds = getFM(values_via_DS, items)


print "Accuracy for MV, WV, EM, DS: ", acc_mv, acc_wv, acc_em, acc_ds
print "F1 measre for MV, WV, EM, DS: ", f1_mv, f1_wv, f1_em, f1_ds





