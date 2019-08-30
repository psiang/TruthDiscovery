import MV
import LFCC
import HisEM
import BCC
import CATD
import PM
import csv
import random
import os
import pandas as pd

run_name = 'PM'
now_work = "d_jnproduct"

def get_truth(e2lpd):
    truth = {}
    for e in e2lpd:
        temp = 0
        for label in e2lpd[e]:
            if temp < e2lpd[e][label]:
                temp = e2lpd[e][label]

        candidate = []

        for label in e2lpd[e]:
            if temp == e2lpd[e][label]:
                candidate.append(label)

        truth[e] = random.choice(candidate)
    return truth

def accurate(wm, truth, day, time, rate):
    ground_truth = pd.read_csv("./data/"+now_work+"/%s/truths/%d/ground_truth_%d.csv" % (rate, time, day), header=0)
    ac_ans = 0
    for j in range(Ntask):
        t = str(ground_truth.iloc[j].loc['task'])
        if t in truth.keys():
            if str(ground_truth.iloc[j].loc['truth']) == truth[t]:
                ac_ans += 1
    ac_ans /= Ntask

    ground_mu = pd.read_csv("./data/"+now_work+"/%s/workers/%d/workers.csv" % (rate, time), header=0)
    RMSRE = 0
    for i in range(len(ground_mu)):
        if wm.get(str(ground_mu.iloc[i].loc['worker']), "None") != "None":
            RMSRE += (ground_mu.iloc[i].loc['value'] - wm[str(ground_mu.iloc[i].loc['worker'])]) ** 2
    RMSRE /= len(wm)
    RMSRE = RMSRE ** 0.5

    RMSTE = 0
    for i in range(len(ground_mu)):
        if wm.get(str(ground_mu.iloc[i].loc['worker']), "None") != "None":
            RMSTE += abs(ground_mu.iloc[i].loc['value'] - wm[str(ground_mu.iloc[i].loc['worker'])])
    RMSTE /= len(wm)

    print("RMSTE", RMSTE, end=' ')
    print("RMSRE", RMSRE, end=' ')
    print("accuracy", ac_ans)


    with open("./result/"+now_work+"/%s/%s/result_%d.csv" % (rate, run_name, time), "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day %d" % day, RMSTE, RMSRE, ac_ans])


def accurate2(e2wl, w2el, label_set, truth, day, time, rate):
    # init_ab
    alph = {}
    beta = {}
    for worker in w2el.keys():
        if alph.get(worker, "None") == "None":
            alph.update({worker: 1})
            beta.update({worker: 1})
    # init_e2lpd
    e2lpd = {}
    for example, worker_label_set in e2wl.items():
        lpd = {}
        total = 0
        for label in label_set:
            lpd[label] = 0

        for (w, label) in worker_label_set:
            lpd[label] += 1
            total += 1

        if not total:
            for label in label_set:
                lpd[label] = 1.0 / len(label_set)
        else:
            for label in label_set:
                lpd[label] = lpd[label] * 1.0 / total

        e2lpd[example] = lpd
    # init_wm
    wm = {}
    for worker in w2el.keys():
        if wm.get(worker, "None") == "None":
            wm.update({worker: 0})
    # update_wm
    for w in w2el.keys():
        wm[w] = 0

    for w in w2el:
        sum_w2lpd = 0
        for example, label in w2el[w]:
            sum_w2lpd += e2lpd[example][label]
        wm[w] = (alph[w] + sum_w2lpd) / (alph[w] + beta[w] + len(w2el[w]))


    ground_truth = pd.read_csv("./data/"+now_work+"/%s/truths/%d/ground_truth_%d.csv" % (rate, time, day), header=0)
    ac_ans = 0
    for j in range(Ntask):
        t = str(ground_truth.iloc[j].loc['task'])
        if t in truth.keys():
            if str(ground_truth.iloc[j].loc['truth']) == truth[t]:
                ac_ans += 1
    ac_ans /= Ntask

    ground_mu = pd.read_csv("./data/"+now_work+"/%s/workers/%d/workers.csv" % (rate, time), header=0)
    RMSRE = 0
    for i in range(len(ground_mu)):
        if wm.get(str(ground_mu.iloc[i].loc['worker']), "None") != "None":
            RMSRE += (ground_mu.iloc[i].loc['value'] - wm[str(ground_mu.iloc[i].loc['worker'])]) ** 2
    RMSRE /= len(wm)
    RMSRE = RMSRE ** 0.5

    RMSTE = 0
    for i in range(len(ground_mu)):
        if wm.get(str(ground_mu.iloc[i].loc['worker']), "None") != "None":
            RMSTE += abs(ground_mu.iloc[i].loc['value'] - wm[str(ground_mu.iloc[i].loc['worker'])])
    RMSTE /= len(wm)

    print("RMSTE", RMSTE, end=' ')
    print("RMSRE", RMSRE, end=' ')
    print("accuracy", ac_ans)


    with open("./result/"+now_work+"/%s/%s/result_%d.csv" % (rate, run_name, time), "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day %d" % day, RMSTE, RMSRE, ac_ans])


def accurate3(truth, day, time, rate):
    ground_truth = pd.read_csv("./data/"+now_work+"/%s/truths/%d/ground_truth_%d.csv" % (rate, time, day), header=0)
    ac_ans = 0
    for j in range(Ntask):
        t = str(ground_truth.iloc[j].loc['task'])
        if t in truth.keys():
            if str(ground_truth.iloc[j].loc['truth']) == truth[t]:
                ac_ans += 1
    ac_ans /= Ntask

    print("accuracy", ac_ans)

    with open("./result/"+now_work+"/%s/%s/result_%d.csv" % (rate, run_name, time), "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day %d" % day, 0, 0, ac_ans])


def update_ab(w2el, truth, alph, beta):
    for w in w2el:
        for example, label in w2el[w]:
            if truth[example] == label:
                alph.update({w: alph[w] + 1})
            else:
                beta.update({w: beta[w] + 1})


if __name__ == '__main__':
    print("Start!")
    rates = ['10', '15', '20', '25', '30', '35', '40']
    for rate in rates:
        if not os.path.exists("./result/" + now_work + "/%s" % rate):
            os.mkdir("./result/" + now_work + "/%s" % rate)
        print(rate + " is starting!")

        for time in range(0, 1):
            if not os.path.exists("./result/" + now_work + "/%s/%s" % (rate, run_name)):
                os.mkdir("./result/" + now_work + "/%s/%s" % (rate, run_name))
            with open("./result/"+now_work+"/%s/%s/result_%d.csv" % (rate, run_name, time), "w", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Day", "RMSTE", "RMSRE", "Accuracy"])

            alph = {}
            beta = {}
            for day in range(0,int(rate)):
                Ntask = 40

                if (run_name == "LFCC"):
                    # LFCC
                    print("%s Day %d:" % (run_name, day))
                    e2wl, w2el, label_set = \
                        LFCC.gete2wlandw2el("./data/"+now_work+"/%s/answers/%d/answer_%d.csv" % (rate, time, day))
                    print('读入数据完毕')
                    e2lpd, wm = LFCC.EM(e2wl, w2el, label_set).Run()
                    print('EM完毕')
                    truth = get_truth(e2lpd)
                    print('get真相完毕')
                    accurate3(truth, day, time, rate)
                    #accurate(wm, truth, day, time, rate)
                    print('acc计算完毕')
                elif (run_name == "HisEM"):
                    # HisEM
                    print("%s Day %d:" % (run_name, day))
                    e2wl, w2el, label_set = \
                        HisEM.gete2wlandw2el("./data/"+now_work+"/%s/answers/%d/answer_%d.csv" % (rate, time, day))
                    print('读入数据完毕')
                    e2lpd, wm = HisEM.EM(alph, beta, e2wl, w2el, label_set).Run()
                    print('EM完毕')
                    truth = get_truth(e2lpd)
                    print('get真相完毕')
                    accurate3(truth, day, time, rate)
                    #accurate(wm, truth, day, time, rate)
                    print('acc计算完毕')
                    update_ab(w2el, truth, alph, beta)
                    print('更新ab完毕')
                elif (run_name == "BCC"):
                    # BCC
                    print("%s Day %d:" % (run_name, day))
                    BCC.gete2wlandw2el("./data/"+now_work+"/%s/answers/%d/answer_%d.csv" % (rate, time, day))
                    print('读入数据完毕')
                    e2lpd = BCC.Run()
                    print('Run完毕')
                    truth = get_truth(e2lpd)
                    print('get真相完毕')
                    accurate3(truth, day, time, rate)
                    print('acc计算完毕')
                elif (run_name == "CATD"):
                    #CATD
                    print("%s Day %d:" % (run_name, day))
                    e2wl, w2el, label_set = CATD.gete2wlandw2el("./data/"+now_work+"/%s/answers/%d/answer_%d.csv" % (rate, time, day))
                    print('读入数据完毕')
                    truth, weight = CATD.Conf_Aware(e2wl, w2el, 'categorical').Run(0.05,100)
                    print('EM完毕')
                    accurate3(truth, day, time, rate)
                    #accurate2(e2wl, w2el, label_set, truth, day, time, rate)
                    print('acc计算完毕')
                elif (run_name == "MV"):
                    #MV
                    print("%s Day %d:" % (run_name, day))
                    e2wl, w2el, label_set = MV.gete2wlandw2el("./data/"+now_work+"/%s/answers/%d/answer_%d.csv" % (rate, time, day))
                    print('读入数据完毕')
                    e2lpd = MV.MV(e2wl, w2el, label_set).Run()
                    print('EM完毕')
                    truth = get_truth(e2lpd)
                    print('get真相完毕')
                    accurate3(truth, day, time, rate)
                    #accurate2(e2wl, w2el, label_set, truth, day, time, rate)
                    print('acc计算完毕')
                elif (run_name == "PM"):
                    # PM
                    print("%s Day %d:" % (run_name, day))
                    e2wl, w2el, label_set = PM.gete2wlandw2el("./data/"+now_work+"/%s/answers/%d/answer_%d.csv" % (rate, time, day))
                    print('读入数据完毕')
                    e2lpd, weight = PM.CRH(e2wl, w2el, label_set, 'categorical', r'0/1 loss').Run(10)
                    print('EM完毕')
                    truth = get_truth(e2lpd)
                    print('get真相完毕')
                    # accurate2(e2wl, w2el, label_set, truth, day, time, rate)
                    accurate3(truth, day, time, rate)
                    print('acc计算完毕')

            print("Time %d Finish!" % time)

            '''print(alph)
            print(beta)
            for key in alph.keys():
                print(key+',' +str(alph[key] / (beta[key] + alph[key])))'''
        print(rate + " is finished!")