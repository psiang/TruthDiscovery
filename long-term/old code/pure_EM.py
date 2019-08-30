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


def init_ab(day, answer, alph, beta):
    for i in range(len(answer.index)):
        if alph.get(int(answer.iloc[i].loc['worker']), "None") == "None":
            alph.update({int(answer.iloc[i].loc['worker']): 1})
            beta.update({int(answer.iloc[i].loc['worker']): 1})


def em(answer, alph, beta):
    # initialize
    task_sum = [0] * Ntask
    pi = [0] * Ntask
    mu = {}
    worker = list(set(answer['worker'].tolist()))
    work_sum = {}
    for w in worker:
        work_sum.update({int(w): 0})
    print("Nworker:", len(worker))

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

    for iter in range(100):
        # E-step
        for w in worker:
            mu[w] = 0
        for i in range(len(answer.index)):
            w = int(answer.iloc[i].loc['worker'])
            t = int(answer.iloc[i].loc['task'])
            a = answer.iloc[i].loc['answer']
            mu.update({w: mu[w] + a * pi[t] + (1 - a) * (1 - pi[t])})
        for w in mu:
            mu.update({w: (mu[w] + alph[w]) / (alph[w] + beta[w] + work_sum[w])})

        # M-step
        pr_x1 = [1] * Ntask
        pr_x0 = [1] * Ntask
        for i in range(len(answer.index)):
            w = int(answer.iloc[i].loc['worker'])
            t = int(answer.iloc[i].loc['task'])
            a = answer.iloc[i].loc['answer']
            if a == 1:
                pr_x1[t] *= mu[w]
                pr_x0[t] *= (1 - mu[w])
            else:
                pr_x1[t] *= (1 - mu[w])
                pr_x0[t] *= mu[w]
        x1 = np.mean(pi)
        x0 = 1 - x1
        pi_new = [0] * Ntask
        for j in range(Ntask):
            pi_new[j] = pr_x1[j] * x1 / (pr_x0[j] * x0 + pr_x1[j] * x1)

        # convergence
        if iter > 0:
            count = 0
            print(pi_new)
            for j in range(Ntask):
                count += (pi[j] - pi_new[j]) ** 2
            count /= Ntask
            if count < 0.0001:
                pi = pi_new
                break
        pi = pi_new

    return mu, pi


def get_truth(pi):
    truth = [0] * Ntask
    for j in range(Ntask):
        if pi[j] > 0.5 or (pi[j] == 0.5 and fliper(0.5)):
            truth[j] = 1
        else:
            truth[j] = 0
    return truth


def accurate(mu, truth, day, time):
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

    with open("./result/LFCC/result_%d.csv" % time, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day %d" % day, RMSTE, RMSRE, ac_ans])


if __name__ == '__main__':
    print("Start!")
    for time in range(98, 100):
        alph = {}
        beta = {}
        with open("./result/LFCC/result_%d.csv" % time, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Day", "RMSTE", "RMSRE", "Accuracy"])

        for day in range(20):
            Ntask = 50
            print("Day %d:" % day)
            answer = read_answer(day, time)
            init_ab(day, answer, alph, beta)
            print('初始化ab完毕')
            mu, pi = em(answer, alph, beta)
            print('EM完毕')
            truth = get_truth(pi)
            print('get真相完毕')
            accurate(mu, truth, day,time)
        print("Time %d Finish!" % time)
