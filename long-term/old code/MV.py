import pandas as pd
import numpy as np
import random
import csv
from scipy.stats import chi2


Ntask = 50


def fliper(p):
    if random.uniform(0, 1) <= p:
        return True
    else:
        return False


def read_answer(day, time):
    data = pd.read_csv("./data/answers/%d/answer_%d.csv" % (time, day), header=0)
    return data


def mv(answer):
    # initialize
    workers = list(set(answer['worker'].tolist()))
    x = [0] * Ntask
    for worker in workers:
        w.update({int(worker): 1})
    print("Nworker:", len(workers))

    for i in range(len(answer.index)):
        task = int(answer.iloc[i].loc['task'])
        ans = answer.iloc[i].loc['answer']
        x[task] += (1 if (ans == 1) else -1)

    return x


def get_truth(x):
    truth = [0] * Ntask
    for j in range(Ntask):
        if x[j] > 0 or (x[j] == 0 and fliper(0.5)):
            truth[j] = 1
        else:
            truth[j] = 0
    return truth


def accurate(answer, truth, day, time):
    task_sum = [0] * Ntask
    pi = [0] * Ntask
    work_sum = {}
    alph = {}
    beta = {}
    worker = list(set(answer['worker'].tolist()))
    for w in worker:
        alph.update({int(w): 1})
        beta.update({int(w): 1})
        work_sum.update({int(w): 0})

    for i in range(len(answer.index)):
        w = int(answer.iloc[i].loc['worker'])
        t = int(answer.iloc[i].loc['task'])
        a = answer.iloc[i].loc['answer']
        pi[t] += a
        task_sum[t] += 1
        work_sum.update({w: work_sum[w] + 1})
    for i in range(Ntask):
        if task_sum[i] != 0:
            pi[i] /= task_sum[i]

    mu = {}
    for w in worker:
        mu[w] = 0
    for i in range(len(answer.index)):
        w = int(answer.iloc[i].loc['worker'])
        t = int(answer.iloc[i].loc['task'])
        a = answer.iloc[i].loc['answer']
        if a == truth[t]:
            alph.update({w: alph[w] + 1})
        else:
            beta.update({w: beta[w] + 1})
        mu.update({w: mu[w] + a * pi[t] + (1 - a) * (1 - pi[t])})
    for w in mu:
        mu.update({w: (mu[w] + alph[w]) / (alph[w] + beta[w] + work_sum[w])})

    ground_truth = pd.read_csv("./data/truths/%d/ground_truth_%d.csv" % (time, day), header=0)
    ac_ans = 0
    for j in range(Ntask):
        if ground_truth.iloc[j].loc['truth'] == truth[j]:
            ac_ans += 1
    ac_ans /= Ntask

    ground_mu = pd.read_csv("./data/workers/%d/workers.csv" % time, header=0)
    RMSRE = 0
    for i in range(len(ground_mu)):
        if mu.get(ground_mu.iloc[i].loc['worker'], "None") != "None":
            RMSRE += (ground_mu.iloc[i].loc['value'] - mu[ground_mu.iloc[i].loc['worker']]) ** 2
    RMSRE /= len(mu)
    RMSRE = RMSRE ** 0.5

    RMSTE = 0
    for i in range(len(ground_mu)):
        if mu.get(ground_mu.iloc[i].loc['worker'], "None") != "None":
            RMSTE += abs(ground_mu.iloc[i].loc['value'] - mu[ground_mu.iloc[i].loc['worker']])
    RMSTE /= len(mu)

    print("RMSTE", RMSTE, end=' ')
    print("RMSRE", RMSRE, end=' ')
    print("accuracy", ac_ans)

    with open("./result/MV/result_%d.csv" % time, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day %d" % day, RMSTE, RMSRE, ac_ans])


if __name__ == '__main__':
    print("Start!")
    for time in range(0, 1):
        x = {}
        w = {}
        with open("./result/MV/result_%d.csv" % time, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Day", "RMSTE", "RMSRE", "Accuracy"])

        for day in range(20):
            Ntask = 50
            print("Day %d:" % day)
            answer = read_answer(day, time)
            print('读取answer完毕')
            x = mv(answer)
            print('EM完毕')
            truth = get_truth(x)
            print('get真相完毕')
            accurate(answer, truth, day,time)
            print('acc计算完毕')
        print("Time %d Finish!" % time)
