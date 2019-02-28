import pandas as pd
import numpy as np
import random
import csv
from scipy.stats import chi2


Nday = 20
Ntask = 100


def fliper(p):
    if random.uniform(0, 1) <= p:
        return True
    else:
        return False


def read_answer(day):
    data = pd.read_csv("./data/answers/answer_%d.csv" % day, header=0)
    return data


def init_ab(day, answer, alph, beta):
    if day == 0:
        for i in range(len(answer.index)):
            if alph.get(int(answer.iloc[i].loc['worker']), "None") == "None":
                alph.update({int(answer.iloc[i].loc['worker']): 1})
                beta.update({int(answer.iloc[i].loc['worker']): 1})
    else:
        mv = []
        for worker in alph.keys():
            w = int(worker)
            mv.append(alph[w] / (alph[w] + beta[w]))
        mv_mean = np.mean(mv)
        mv_var = np.var(mv) * len(mv) / (len(mv) - 1)

        lamda = mv_mean
        sigma = ((len(mv) - 1) * mv_var / chi2.isf(0.025, len(mv) - 1) +
                 (len(mv) - 1) * mv_var / chi2.isf(0.975, len(mv) - 1)) / 2

        new_alph = (1 - lamda) * lamda ** 2 / sigma - lamda
        new_beta = (1 - lamda) ** 2 * lamda / sigma - (1 - lamda)

        for i in range(len(answer.index)):
            if alph.get(int(answer.iloc[i].loc['worker']), "None") == "None":
                alph.update({int(answer.iloc[i].loc['worker']): new_alph})
                beta.update({int(answer.iloc[i].loc['worker']): new_beta})


def em(answer, alph, beta):
    # initialize
    task_sum = [0] * Ntask
    pi = [0] * Ntask
    mu = {}
    worker = list(set(answer['worker'].tolist()))
    print("Nworker:", len(worker))
    for i in range(len(answer.index)):
        pi[int(answer.iloc[i].loc['task'])] += answer.iloc[i].loc['answer']
        task_sum[int(answer.iloc[i].loc['task'])] += 1
    for i in range(Ntask):
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
            mu.update({w: (mu[w] + alph[w]) / (alph[w] + beta[w] + Ntask)})

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


def accurate(mu, truth, day):
    ground_truth = pd.read_csv("./data/truths/ground_truth_%d.csv" % (day), header=0)
    ac_ans = 0
    for j in range(Ntask):
        if ground_truth.iloc[j].loc['truth'] == truth[j]:
            ac_ans += 1
    ac_ans /= Ntask

    ground_mu = pd.read_csv("./data/workers.csv", header=0)
    mse_mu = 0
    for i in range(len(ground_mu)):
        if mu.get(ground_mu.iloc[i].loc['worker'], "None") != "None":
            mse_mu += (ground_mu.iloc[i].loc['value'] - mu[ground_mu.iloc[i].loc['worker']]) ** 2
    mse_mu /= len(mu)

    print("mse_mu ", mse_mu, end=' ')
    print("accuracy", ac_ans)

    with open("./result.csv","a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day %d" % day, mse_mu, ac_ans])


def update_ab(answer, truth, alph, beta):
    for i in range(len(answer)):
        w = int(answer.iloc[i].loc['worker'])
        t = int(answer.iloc[i].loc['task'])
        a = int(answer.iloc[i].loc['answer'])
        if a == truth[t]:
            alph.update({w: alph[w] + 1})
        else:
            beta.update({w: beta[w] + 1})


if __name__ == '__main__':
    alph = {}
    beta = {}
    with open("./result.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Day", "MSE_mu", "Accuracy"])

    for day in range(20):
        print("Day %d:" % day)
        answer = read_answer(day)
        init_ab(day, answer, alph, beta)
        print('初始化ab完毕')
        mu, pi = em(answer, alph, beta)
        print('EM完毕')
        truth = get_truth(pi)
        print('get真相完毕')
        accurate(mu, truth, day)
        update_ab(answer, truth, alph, beta)
        print('更新ab完毕')
