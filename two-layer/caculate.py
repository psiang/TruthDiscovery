import ZC
import LFC
import csv
import math
import random


def getaccuracy(truthfile, e2lpd):
    e2truth = {}
    f = open(truthfile, 'r')
    reader = csv.reader(f)
    next(reader)

    for line in reader:
        example, truth = line
        e2truth[example] = truth

    tcount = 0
    count = 0

    for e in e2lpd:

        if e not in e2truth:
            continue

        temp = 0
        for label in e2lpd[e]:
            if temp < e2lpd[e][label]:
                temp = e2lpd[e][label]

        candidate = []

        for label in e2lpd[e]:
            if temp == e2lpd[e][label]:
                candidate.append(label)

        truth = random.choice(candidate)

        count += 1

        if truth == e2truth[e]:
            tcount += 1

    return tcount*1.0/count


# 找到对应分布类型的等价参数
def random_pr(pr, style):
    pf = 0
    if style == "Uniform":
        a = 0
        b = pr
        pf = random.uniform(a, b)
    elif style == "Beta":
        alpha = pr
        beta = 1 - pr
        pf = random.betavariate(alpha, beta)
    elif style == "Exponential":
        lambd = pr
        pf = random.expovariate(lambd)
        if pf > 1:
            pf = 1
    elif style == "Gamma":
        alpha = pr
        beta = 1
        pf = random.gammavariate(alpha, beta)
        if pf > 1:
            pf = 1
    return pf


# 找到对应分布类型的等价参数
def equal_pr(e, style):
    if style == "Uniform":
        return 2 / (math.exp(e) + 1)
    elif style == "Beta":
        return 1 / (math.exp(e) + 1)
    elif style == "Exponential":
        return math.exp(e) + 1
    elif style == "Gamma":
        return 1 / (math.exp(e) + 1)


# 判断概率是否发生
def flip_or_not(prob):
    if random.random() <= prob:
        return 1
    else:
        return 0


# onelayer加噪
def perturb_onelayer(data_file, label_set, pf):
    e2wl = {}
    w2el = {}

    f = open(data_file, 'r')
    reader = csv.reader(f)
    next(reader)

    for line in reader:
        example, worker, label = line
        if flip_or_not(pf):
            to_list = [k for k in label_set if k != label]
            label = random.choice(to_list)
        if example not in e2wl:
            e2wl[example] = []
        e2wl[example].append([worker,label])

        if worker not in w2el:
            w2el[worker] = []
        w2el[worker].append([example,label])

        if label not in label_set:
            label_set.append(label)

    return e2wl,w2el


# twolayer加噪
def perturb_twolayer(data_file, label_set, pr, style):
    e2wl = {}
    w2el = {}
    worker_pf = {}

    f = open(data_file, 'r')
    reader = csv.reader(f)
    next(reader)

    for line in reader:
        example, worker, label = line
        if worker not in worker_pf:
            worker_pf[worker] = random_pr(pr, style)
        if flip_or_not(worker_pf[worker]):
            to_list = [k for k in label_set if k != label]
            label = random.choice(to_list)
        if example not in e2wl:
            e2wl[example] = []
        e2wl[example].append([worker,label])

        if worker not in w2el:
            w2el[worker] = []
        w2el[worker].append([example,label])

        if label not in label_set:
            label_set.append(label)

    return e2wl,w2el


def gete2wlandw2el(datafile):
    e2wl = {}
    w2el = {}
    label_set=[]

    f = open(datafile, 'r')
    reader = csv.reader(f)
    next(reader)

    for line in reader:
        example, worker, label = line
        if example not in e2wl:
            e2wl[example] = []
        e2wl[example].append([worker,label])

        if worker not in w2el:
            w2el[worker] = []
        w2el[worker].append([example,label])

        if label not in label_set:
            label_set.append(label)

    return e2wl,w2el,label_set


def execute(data_file, truth_file):
    e2wl, w2el, label_set = gete2wlandw2el(data_file)
    e2lpd, wm = LFC.EM(e2wl, w2el, label_set).Run()
    accuracy = getaccuracy(truth_file, e2lpd)
    print(accuracy)

    n = 10
    style = 'Uniform'
    e_list_origin = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.001, 0.0]

    if style == 'Exponential':
        e_list = [0.9648513868451118, 0.8475331654689704, 0.730388397937257,
                  0.6097469478991127, 0.48101835901641726, 0.34337225181842174,
                  0.19847853464215953, 0.043426372091174004, -0.12310288754782026,
                  -0.3106643476053096, -0.4978324695829641, -0.5176191828087624,
                  -0.522867381837526]
    elif style == "Gamma":
        e_list = [0.6369664713130023, 0.5117903314858268, 0.382904052734375,
                  0.24208450247533614, 0.10788107617986577, -0.040507247958678286,
                  -0.1987433713366052, -0.3617469326063796, -0.5386977658320813,
                  -0.7367098941658703, -0.9384765625, -0.9521432715541753,
                  -0.9541385503868145]
    else:
        e_list = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.01, 0.001, 0.0]
    for e in e_list:
        print(e_list_origin[e_list.index(e)], end='\t')
        pf = 1 / (math.exp(e) + 1)
        pr = equal_pr(e, style)

        # ZC with one-layer
        acc_onelayer = 0.0
        for i in range(n):
            e2wl_perturb, w2el_perturb = perturb_onelayer(data_file, label_set, pf)
            e2lpd_perturb, wm_perturb = LFC.EM(e2wl_perturb, w2el_perturb, label_set).Run()
            acc_onelayer += getaccuracy(truth_file, e2lpd_perturb)
            del e2wl_perturb
            del w2el_perturb
            del e2lpd_perturb
            del wm_perturb
        acc_onelayer /= n
        print(round(acc_onelayer, 8), end='\t')

        # ZC with two-layer
        acc_twolayer = 0.0
        for i in range(n):
            e2wl_perturb, w2el_perturb = perturb_twolayer(data_file, label_set, pr, style)
            e2lpd_perturb, wm_perturb = LFC.EM(e2wl_perturb, w2el_perturb, label_set).Run()
            acc_twolayer += getaccuracy(truth_file, e2lpd_perturb)
            del e2wl_perturb
            del w2el_perturb
            del e2lpd_perturb
            del wm_perturb
        acc_twolayer /= n
        print(round(acc_twolayer, 8), end='\n')

